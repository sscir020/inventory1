create database testdb1;
use testdb1;
create table users(
		user_id int not null auto_increment,
		user_name varchar(64) not null,
		user_pass varchar(64) not null,
		role int not null default 1 ,
		primary key (user_id),
		unique(user_name)
		)default charset=utf8;

drop table if exists accessories;
create table accessories(
        acces_id int not null auto_increment,
        param_num int not null,
        param_acces varchar(2048) not null,
        primary key (acces_id)
        unique(acces_id)
)default charset=utf8;

drop table if EXISTS oprs;
drop table if exists materials;

create table materials(
		material_id int not null auto_increment,
		material_name varchar(64) not null,
		storenum int not null default 0,
        restorenum int not null default 0,
        scrapnum int not null default 0,
        preparenum int not null default 0,
        salenum int not null default 0,
        resalenum int not null default 0,
		alarm_level int not null default 0,
		acces_id int not null default 0,
		primary key (material_id),
		unique(material_name)
		)default charset=utf8;
drop table if exists buys;

create table buys(
        buy_id int not null auto_increment,
        batch varchar(32) not null,
        material_id int not null,
        num int not null default 0,
        comment varchar(64) default '',
        primary key(buy_id),
        unique(batch),
        foreign key (material_id) references materials(material_id)
)default charset=utf8;

drop table if exists reworks;
create table reworks(
        rework_id int not null auto_increment,
        material_id int,
        service_id int,
        MN_id varchar(32) not null default '',
		batch varchar(32) not null,
        num int not null default 0,
        comment varchar(64) default '',
        primary key(rework_id),
        unique(batch),
        foreign key (material_id) references materials(material_id),
        foreign key (service_id) references Customerservice(service_id)
)default charset=utf8;

drop table if EXISTS clients;
drop table if exists devices;
create table devices(
        device_id int not null auto_increment,
        MN_id varchar(32) not null default '',
        device_type varchar(20) not null,
        device_name varchar(32) not null default '',
        storenum int not null default 0,
        preparenum int not null default 0,
        salenum int not null default 0,
        resalenum int not null default 0,
        acces_id int null default 0,
        comment varchar(64) default '',
        primary key(device_id),
        unique(MN_id),
        foreign key (acces_id) references accessories(acces_id)
)default charset=utf8;
create table clients(
        client_id int not null auto_increment,
        client_name varchar(32) not null,
        MN_id varchar(32) not null default '',
        credit int not null default 0,
        comment varchar(64) default '',
        primary key(client_id),
        unique(client_name),
        unique(MN_id)
)default charset=utf8;
drop table  if exists oprs;
create table oprs(
		opr_id int not null auto_increment,
		user_id int not null,
		material_id int null,
		device_id int null,
		client_id int null,
		service_id int null,
		MN_id varchar(32) default '',
		diff int not null default 0,
		oprtype varchar(32) not null,
		oprbatch varchar(32) not null default '',
		isgroup tinyint(1) not null default 0,
		comment varchar(64) default '',
		momentary datetime not null default current_timestamp,
		primary key (opr_id),
		unique(opr_id),
		foreign key (user_id) references users(user_id),
		foreign key (material_id) references materials(material_id),
		foreign key (device_id) references devices(device_id),
		foreign key (client_id) references clients(client_id),
		foreign key (service_id) references customerservice(service_id)
		)default charset=utf8;

create table customerservice(
        service_id  int not null auto_increment,
        MN_id varchar(32) not null default '',
        material_id int,
        device_id int,
        originnum int not null default 0,
        goodnum int not null default 0,
        brokennum int not null default 0,
        reworknum int not null default 0,
        restorenum int not null default 0,
        scrapnum int not null default 0,
        inboundnum int not null default 0,
        resalenum int not null default 0,
        fee int not null default 0,
        comment varchar(64) default '',
        isold tinyint(1) default 0,
        primary key(service_id),
		unique(service_id),
		foreign key (material_id) references materials(material_id)
)default charset=utf8;


alter table materials convert to character set utf8 collate utf8_unicode_ci;
alter table users convert to character set utf8 collate utf8_unicode_ci;
alter table buys convert to character set utf8 collate utf8_unicode_ci;
alter table reworks convert to character set utf8 collate utf8_unicode_ci;
alter table accessories convert to character set utf8 collate utf8_unicode_ci;
alter table oprs convert to character set utf8 collate utf8_unicode_ci;
alter table device convert to character set utf8 collate utf8_unicode_ci;
alter table client convert to character set utf8 collate utf8_unicode_ci;

#default-character-set=utf8
#character-set-server=utf8
SET character_set_database =utf8;
SET character_set_results =utf8;
SET character_set_server =utf8;
SET character_set_system =utf8; 
#/*�˴�utf-8Ҳ����*/
SET collation_server = utf8_general_ci;
SET collation_database = utf8_general_ci;


alter table materials add COLUMN preparenum int not null default 0;
alter table devices drop column preparenum;

create table fruit(
		fruit_id int not null auto_increment PRIMARY key,
		fruit_name varchar(10) not null
);

create table total(
		total_id int not null auto_increment PRIMARY KEY,
		item_id int,
		fruit_id int

)

alter table devices modify MN_id varchar(32) not null;
alter table devices add unique(MN_id);

insert into users(user_name,user_pass) values('zhang','1234');
insert into users(user_name,user_pass) values('wang','1234');
insert into users(user_name,user_pass) values('zhao','1234');

insert into materials(material_name,countnum) values('apple',20);
insert into materials(material_name,countnum) values('orange',30);
insert into materials(material_name,countnum) values('banana',25);
insert into materials(material_name,countnum) values('strawberry',35);
insert into materials(material_name,countnum) values('apple1',20);
insert into materials(material_name,countnum) values('orange1',30);
insert into materials(material_name,countnum) values('banana1',25);
insert into materials(material_name,countnum) values('strawberry1',35);
insert into materials(material_name,countnum) values('apple2',20);
insert into materials(material_name,countnum) values('orange2',30);
insert into materials(material_name,countnum) values('banana2',25);
insert into materials(material_name,countnum) values('strawberry2',35);
insert into materials(material_name,countnum) values('apple3',20);
insert into materials(material_name,countnum) values('orange3',30);
insert into materials(material_name,countnum) values('banana3',25);
insert into materials(material_name,countnum) values('strawberry3',35);

insert into oprs(user_id,material_id,diff,oprtype) values (2,1,20,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (1,3,25,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (3,4,35,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (2,2,30,"INITADD");

insert into oprs(user_id,material_id,diff,oprtype) values (2,1,20,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (1,3,25,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (3,4,35,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (2,2,30,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (2,1,20,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (1,3,25,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (3,4,35,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (2,2,30,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (2,1,20,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (1,3,25,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (3,4,35,"INITADD");
insert into oprs(user_id,material_id,diff,oprtype) values (2,2,30,"INITADD");
