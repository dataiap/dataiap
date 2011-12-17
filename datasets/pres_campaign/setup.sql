drop table if exists donations;
create table donations(name varchar(128), 
  date date,
  amount float, 
  state varchar(40),
  zipcode varchar(10),
  job varchar(30),
  reason varchar(128),
  memo varchar(128)
  );
.separator ","
.import donations.csv donations
create index idx_name on donations(name);
create index idx_name_reason on donations(name,reason);
create index idx_state on donations(state);
create index idx_job on donations(job);