import os, email, re, dateutil
from dateutil.parser import parse as parsedate
from collections import defaultdict


STOPWORDS = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])



class Email(object):
    refs_pat = '<?(?P<ref>.+)>?'
    refs_prog = re.compile(refs_pat)
    contacts_pat = '(([\"\']?(?P<realname>\w[\w\ ]*)[\"\']?)?\s+)?<?(?P<email>[\w.]+@([\w_]+.)+[\w_]+)>?'
    contacts_prog = re.compile(contacts_pat)

    def __init__(self, fpath):
        self.fpath = fpath
        self.fname = os.path.basename(fpath)
        self.folder = os.path.basename(os.path.dirname(fpath))        
        self.load()

    def load(self):
        with file(self.fpath) as f:
            filecontents = f.read()
            e = email.message_from_string( filecontents )
            text = e.get_payload()
            self.text = text.replace('\n\r', '\n').replace("\r", '')
            self.sender =  self.extract_names(e['From'])[0]
            
            #break apart the headers of each email using methods generated in this same script
            self.to = self.extract_names(e.get('To', '')) 
            self.cc = self.extract_names(e.get('CC', ''))
            self.bcc = self.extract_names(e.get('BCC', ''))
            self.recipients = []
            self.recipients.extend(self.to)
            self.recipients.extend(self.cc)
            self.recipients.extend(self.bcc)

            self.subject = e.get('Subject', '')
            self.date = self.clean_date(e['Date'])
            self.mid = self.extract_refs(e.get('Message-ID', ''))[0]
            replyto = self.extract_refs(e.get('In-Reply-To', ''))
            self.replyto = replyto and replyto[0] or None

            if self.date.year == 1979:
                raise RuntimeError
            ctype = e.get('Content-type', '')
            if ctype != '' and 'text/plain' not in ctype:
                raise RuntimeError
            self.ctype = ctype
                
    def clean_date(self, txt):
        if '(' in txt:
            txt = txt[:txt.index('(')]
        return parsedate(txt)

    def clean(self, txt):
        return txt.replace('\r\n',',')

    def extract_refs(self, txt):
        txt = self.clean(txt)
        refs = []
        for block in txt.strip(' ,').split(','):
            res = Email.refs_prog.search(block)
            if res:
                ref = res.group('ref')
                if ref.endswith('>'):
                    ref = ref[:-1]
                refs.append(ref)
        return refs


    def extract_names(self, txt):
        txt = self.clean(txt)
        emails = set()
        contacts = []
        for block in txt.strip(' ,').split(','):
            res = Email.contacts_prog.search(block)
            if res:
                name = res.group('realname')
                email = res.group('email')
                if email: email = email.lower()
                if email in emails: continue
                emails.add(email)
                #contacts.append((name, email))
                contacts.append(email)

        return contacts


class EmailWalker(object):

    def __init__(self, root):
        self.root = root
        self.curdir = None

    def __iter__(self):
        class EmailIter():
            def __init__(self, walker):
                self.w = walker
                self.g = self.generator()

            def generator(self):
                for root, dir, files in os.walk(self.w.root):
                    folder = os.path.basename(root)
                    for fname in files:
                        try:
                            yield Email(os.path.join(root, fname))
                        except:
                            pass
                
            def next(self):
                for retval in self.g:
                    return retval
                raise StopIteration

        return EmailIter(self)


if __name__ == '__main__':
    import sys
    
    w = EmailWalker(sys.argv[1])
    ns = defaultdict(lambda:0)
    for x in w:
        ns[x.date.date()] += 1

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(30, 10))
    subplot = fig.add_subplot(111)

    xs, ys = zip(*sorted(ns.items(), key=lambda (email, c): email))
    ys = [sum(ys[:idx+1]) for idx in xrange(len(ys))]
    subplot.plot(xs, ys)
    subplot.set_xlim(min(xs), max(xs))
    plt.savefig('/tmp/test.png', format='png')
        


