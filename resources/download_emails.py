import base64, hmac, imaplib, csv, random, sha, smtplib, sys, time, urllib
from optparse import OptionParser
from collections import defaultdict
import email, math, threading, pyparsing
from dateutil.parser import parse
from datetime import datetime, timedelta
from pyparsing import (nestedExpr, Literal, Word, alphanums, 
                       quotedString, replaceWith, nums, removeQuotes)



# body structure parser
NIL = Literal("NIL").setParseAction(replaceWith(None))
integer = Word(nums).setParseAction(lambda t:int(t[0]))
quotedString.setParseAction(removeQuotes)
content = (NIL | integer | Word(alphanums))
ne = nestedExpr(content=content, ignoreExpr=quotedString)
bs_parser = ne


def parse_bs(bs):
    """
    parse the string that describes the body structure so we know where to find the text/plain version of the email.  that way we can avoid downloading HTML and attachments.
    """
    try:
        # remove body header content, and close tag
        bs = bs[:bs.rfind('BODY[HEADER]')] + ')'
        # remove outer layer
        bs = bs[ bs.find("(BODYSTRUCTURE") + len("(BODYSTRUCTURE"):bs.rfind(')')].strip()
        ps = bs_parser.parseString(bs)
        struct = ps[0]
        return struct
    except:
        pass


def find_text(bs, prefix=''):
    """
    actual function that parse_bs() calls to do the finding
    """
    if isinstance(bs, pyparsing.ParseResults):
        if bs[0] == 'TEXT' and bs[1] == 'PLAIN':
            if prefix == '':
                section = 'TEXT'
            else:
                section = prefix[1:]
            return section
        else:
            i = 1
            for x in bs:
                ret = find_text(x, '%s.%d' % (prefix, i))
                if ret is not None: return ret
                i += 1



def download_emails(user, passw, host="imap.googlemail.com"):
    """
    connect to gmail and download all headrs since jan-2011
    
    example gmail labels:
     INBOX
     [Gmail]/All Mail
     [Gmail]/Sent Mail

    search_string examples:
     (ALL)
     (BEFORE 20-Apr-2010 SINCE 1-Apr-2010)
     (SUBJECT "atwoods")
     (SINCE 01-Jan-2011)
    """
    #download for a year. depending on the host, use different label_string
    search_string = "(SINCE 1-Jan-2010)"
    search_string = "(ALL)"

    imap_conn = imaplib.IMAP4_SSL(host)
    imap_conn.debug = 0
    labels = []
    try:
        imap_conn.login(user, passw)

        # list all of the folders using imap_conn.list()
        for row in csv.reader(imap_conn.list()[1], delimiter=' '):
            labelname = row[-1]
            metadata = ' '.join(row[:-2])
            # we want to ignore meta-folders and default [Gmail] labels
            if '[Gmail]' not in labelname and '(\\HasNoChildren)' == metadata:
                labels.append(labelname)
                
    except Exception, err:
        import traceback
        print >> sys.stderr, err
        traceback.print_tb(sys.exc_info()[2])
        print >> sys.stderr, ''
        return False


    # create the root folder if it doesn't exist
    try:
        root = './%s' % user
        os.mkdir(root)
    except:
        pass

    # iterate through the labels/folders.
    # Create a folder if it doesn't exist
    # download the emails!
    for label in labels:
        download_folder(imap_conn, label, root, search_string)


def download_folder(imap_conn, label, root, search_string, chunk=1000, maxmsgs=None):
    print "Downloading:", label
    try:
        dirname = os.path.join(root, label)
        os.mkdir(dirname)
    except:
        pass
    
    imap_conn.select(label)
    typ, dat = imap_conn.search(None, search_string)
    iternum = 0

    # profiling information - understand how much time it takes to download the entire headers for the database
    cost = 0.0
    
    # take information and find the number of emails that are downloaded.
    # dat[0] is the list of message ids on the IMAP server
    # cast them to ints and sort them
    mids = sorted(map(int, dat[0].split()))
    print '%d total messages left' % len(mids)
    
    if len(mids) == 0:
        return

    d = None
    filenameindex = 1 # file name.

    # process the mids in batches of 1000.
    # fetch() for 1000 headers at a time.
    try:
        for idx in xrange(0, int(math.ceil(float(len(mids))/chunk))):
            print "processing messages %d - %d" % (idx*chunk, min((idx+1) * chunk,len(mids)))            
            curids = mids[int(idx*chunk):int((idx*chunk)+chunk)]
            if len(curids) == 0:
                continue


            # this only downloads the header information
            # we don't download email contents or attachments here
            typ, dat = imap_conn.fetch(','.join(map(str,curids)), '(BODY.PEEK[HEADER] BODYSTRUCTURE)')

            # map email section -> mid
            # section == None if there is no message body
            textsections = defaultdict(list)

            start = time.time()
            for d in dat:
                if d == ')': continue
                mid = int(d[0][:d[0].find(' ')])

                # this parses the body structure (bs) so we know what section
                # of the body structure contains the email text contents
                # This way we avoid downloading attachments and HTML formatted emails.
                bs_str = d[0]
                bs = parse_bs(bs_str)
                if not bs:
                    # this means the email only had a subject line and no body
                    section = None
                else:
                    section = find_text(bs) or None

                # also remember the mid and the email header text
                textsections[section].append( (mid, d[1]) )

            # loop through the text sections and download them in bulk.
            for section, headerdatas in textsections.iteritems():

                # create a list of email text
                tmpmids, headers = zip(*headerdatas)
                if section == None:
                    texts = [''] * len(tmpmids)
                else:
                    t,d = imap_conn.fetch(','.join(map(str,tmpmids)), '(body.peek[%s])' % section)
                    texts = []
                    for resp in d:
                        if len(resp) > 1:
                            texts.append(email.message_from_string(resp[1]).get_payload())


                # iterate through each email and write it to the proper file
                print '\t', section, len(tmpmids), len(texts)
                for mid, header, text in zip(tmpmids, headers, texts):
                    text = text.replace('\n\r', '\n').replace("\r", '')
                    filename = os.path.join(dirname, '%d.' % filenameindex)
                    with file(filename, 'w') as f:
                        f.write(header)
                        f.write('\n')
                        f.write(text)
                    filenameindex += 1



                if maxmsgs and iternum >= maxmsgs: break
                iternum += 1

            cost += time.time() - start
            if maxmsgs and iternum >= maxmsgs: break
            print "time: %f" % cost
            

    except Exception, err:
        raise
        import traceback
        print >> sys.stderr, err
        traceback.print_tb(sys.exc_info()[2])
        print >> sys.stderr, ''

    print "time: %f" % cost


                            

if __name__ == '__main__':
    import getpass, sys, os, argparse


    # setup arguments
    parser = argparse.ArgumentParser(description="Download emails from an IMAP enabled email server.")
    parser.add_argument('imaphost', metavar='imaphost', type=str, nargs='?',
                        default='imap.googlemail.com', help="hostname of IMAP email server")
    parser.add_argument('-u', nargs='?', dest="username", help="the username")
    parser.add_argument('-p', nargs='?', dest="password", help="your password")


    args = parser.parse_args()
    host = args.imaphost
    username = args.username
    passw = args.password
    if not username:
        username = raw_input("Enter your username on %s: " % host)
    if not passw:
        passw = getpass.getpass("Enter your password for %s@%s: " % (username, host))
        
    print """downloading emails in all labels except for [Gmail] default labels
such as Sent, and All Mail"""
    print "this may take a long time!"
    download_emails(username, passw, host=host)

