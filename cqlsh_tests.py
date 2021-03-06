# -*- coding: utf-8 -*-
from dtest import Tester, debug
from tools import since, require
from ccmlib import common
import subprocess
import binascii
from decimal import Decimal
import sys, os
from uuid import UUID

class TestCqlsh(Tester):

    def __init__(self, *args, **kwargs):
        Tester.__init__(self, *args, **kwargs)

    def test_simple_insert(self):

        self.cluster.populate(1)
        self.cluster.start()

        node1, = self.cluster.nodelist()

        node1.run_cqlsh(cmds = """
            CREATE KEYSPACE simple WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
            use simple;
            create TABLE simple (id int PRIMARY KEY , value text ) ;
            insert into simple (id, value) VALUES (1, 'one');
            insert into simple (id, value) VALUES (2, 'two');
            insert into simple (id, value) VALUES (3, 'three');
            insert into simple (id, value) VALUES (4, 'four');
            insert into simple (id, value) VALUES (5, 'five')""")

        cursor = self.patient_cql_connection(node1).cursor()
        cursor.execute("select id, value from simple.simple");

        self.assertEqual({1:'one', 2:'two', 3:'three', 4:'four', 5:'five'}, 
                         {k : v for k,v in cursor})

    def test_eat_glass(self):
        
        self.cluster.populate(1)
        self.cluster.start()

        node1, = self.cluster.nodelist()

        node1.run_cqlsh(cmds = u"""create KEYSPACE testks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
use testks;

CREATE TABLE varcharmaptable ( 
        varcharkey varchar , 
        varcharasciimap map<varchar, ascii>,
        varcharbigintmap map<varchar, bigint>,
        varcharblobmap map<varchar, blob>,
        varcharbooleanmap map<varchar, boolean>,
        varchardecimalmap map<varchar, decimal>,
        varchardoublemap map<varchar, double>,
        varcharfloatmap map<varchar, float>,
        varcharintmap map<varchar, int>,
        varcharinetmap map<varchar, inet>,
        varchartextmap map<varchar, text>,
        varchartimestampmap map<varchar, timestamp>,
        varcharuuidmap map<varchar, uuid>,
        varchartimeuuidmap map<varchar, timeuuid>,
        varcharvarcharmap map<varchar, varchar>,
        varcharvarintmap map<varchar, varint>,
        PRIMARY KEY (varcharkey));

INSERT INTO varcharmaptable (varcharkey, varcharasciimap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': 'My','Можам да јадам стакло, а не ме штета.': 'Name','I can eat glass and it does not hurt me': 'Is'} );

UPDATE varcharmaptable SET varcharasciimap = varcharasciimap + {'Vitrum edere possum, mihi non nocet.':'Cassandra'} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varcharasciimap['Vitrum edere possum, mihi non nocet.'] = 'Hello' WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

INSERT INTO varcharmaptable (varcharkey, varcharbigintmap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': -45,'Можам да јадам стакло, а не ме штета.': 12300,'I can eat glass and it does not hurt me': 0} );

UPDATE varcharmaptable SET varcharbigintmap = varcharbigintmap + {'Vitrum edere possum, mihi non nocet.':23} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varcharbigintmap['Vitrum edere possum, mihi non nocet.'] = 5100003 WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

INSERT INTO varcharmaptable (varcharkey, varcharblobmap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': 0xDEADBEEF,'Можам да јадам стакло, а не ме штета.': 0xBEEFBEEF,'I can eat glass and it does not hurt me': 0xFEEB} );

UPDATE varcharmaptable SET varcharblobmap = varcharblobmap + {'Vitrum edere possum, mihi non nocet.':0x10} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varcharblobmap['Vitrum edere possum, mihi non nocet.'] = 0xFEED103A WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

INSERT INTO varcharmaptable (varcharkey, varcharbooleanmap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': FALSE,'Можам да јадам стакло, а не ме штета.': FALSE,'I can eat glass and it does not hurt me': FALSE} );

UPDATE varcharmaptable SET varcharbooleanmap = varcharbooleanmap + {'Vitrum edere possum, mihi non nocet.':TRUE} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varcharbooleanmap['Vitrum edere possum, mihi non nocet.'] = TRUE WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

INSERT INTO varcharmaptable (varcharkey, varchardecimalmap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': -20.4,'Можам да јадам стакло, а не ме штета.': 11234234.3,'I can eat glass and it does not hurt me': 10.0} );

UPDATE varcharmaptable SET varchardecimalmap = varchardecimalmap + {'Vitrum edere possum, mihi non nocet.':0.0} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varchardecimalmap['Vitrum edere possum, mihi non nocet.'] = 50.0 WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

INSERT INTO varcharmaptable (varcharkey, varchardoublemap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': -432.311,'Можам да јадам стакло, а не ме штета.': 3.1415,'I can eat glass and it does not hurt me': 20000.0} );

UPDATE varcharmaptable SET varchardoublemap = varchardoublemap + {'Vitrum edere possum, mihi non nocet.':11} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varchardoublemap['Vitrum edere possum, mihi non nocet.'] = 4234243 WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

INSERT INTO varcharmaptable (varcharkey, varcharfloatmap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': -234.3,'Можам да јадам стакло, а не ме штета.': -234234,'I can eat glass and it does not hurt me': 1000.5} );

UPDATE varcharmaptable SET varcharfloatmap = varcharfloatmap + {'Vitrum edere possum, mihi non nocet.':-3.14} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varcharfloatmap['Vitrum edere possum, mihi non nocet.'] = 10.0 WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

INSERT INTO varcharmaptable (varcharkey, varcharintmap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': 2,'Можам да јадам стакло, а не ме штета.': -3,'I can eat glass and it does not hurt me': -500} );

UPDATE varcharmaptable SET varcharintmap = varcharintmap + {'Vitrum edere possum, mihi non nocet.':20000} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varcharintmap['Vitrum edere possum, mihi non nocet.'] = 1 WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

INSERT INTO varcharmaptable (varcharkey, varcharinetmap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': '127.0.0.1','Можам да јадам стакло, а не ме штета.': '8.8.8.8','I can eat glass and it does not hurt me': '8.8.4.4'} );

UPDATE varcharmaptable SET varcharinetmap = varcharinetmap + {'Vitrum edere possum, mihi non nocet.':'241.30.12.24'} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varcharinetmap['Vitrum edere possum, mihi non nocet.'] = '192.168.0.1' WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

INSERT INTO varcharmaptable (varcharkey, varchartextmap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': 'On a trip','Можам да јадам стакло, а не ме штета.': 'Across','I can eat glass and it does not hurt me': 'The '} );

UPDATE varcharmaptable SET varchartextmap = varchartextmap + {'Vitrum edere possum, mihi non nocet.':'Sea'} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varchartextmap['Vitrum edere possum, mihi non nocet.'] = 'Once I went' WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

INSERT INTO varcharmaptable (varcharkey, varchartimestampmap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': '1985-08-03T04:21:01+0000','Можам да јадам стакло, а не ме штета.': '2000-01-01T00:20:01+0000','I can eat glass and it does not hurt me': '1942-03-11T5:21:01+0000'} );

UPDATE varcharmaptable SET varchartimestampmap = varchartimestampmap + {'Vitrum edere possum, mihi non nocet.':'2043-11-04T11:21:01+0000'} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varchartimestampmap['Vitrum edere possum, mihi non nocet.'] = '2013-06-19T03:21:01+0000' WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

INSERT INTO varcharmaptable (varcharkey, varcharuuidmap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': 1df0b6ac-f3d3-456c-8b78-2bc70e585107,'Можам да јадам стакло, а не ме штета.': e2ed2164-31dc-42cb-8ee9-47376e071210,'I can eat glass and it does not hurt me': a487fe45-8af5-4454-ac66-2614286d7e89} );

UPDATE varcharmaptable SET varcharuuidmap = varcharuuidmap + {'Vitrum edere possum, mihi non nocet.':d25bdfc7-eb81-472c-bf5b-b4e6afdf66c2} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varcharuuidmap['Vitrum edere possum, mihi non nocet.'] = 7787064c-ce54-4324-abdd-05775b89ead7 WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

INSERT INTO varcharmaptable (varcharkey, varchartimeuuidmap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': 670c7f90-d8ec-11e2-a28f-0800200c9a66,'Можам да јадам стакло, а не ме штета.': 750c2d70-d8ec-11e2-a28f-0800200c9a66,'I can eat glass and it does not hurt me': 80d74810-d8ec-11e2-a28f-0800200c9a66} );

UPDATE varcharmaptable SET varchartimeuuidmap = varchartimeuuidmap + {'Vitrum edere possum, mihi non nocet.':93e276f0-d8ec-11e2-a28f-0800200c9a66} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varchartimeuuidmap['Vitrum edere possum, mihi non nocet.'] = 4a36c100-d8ec-11e2-a28f-0800200c9a66 WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

INSERT INTO varcharmaptable (varcharkey, varcharvarcharmap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑','Можам да јадам стакло, а не ме штета.': 'Можам да јадам стакло, а не ме штета.','I can eat glass and it does not hurt me': 'I can eat glass and it does not hurt me'} );

UPDATE varcharmaptable SET varcharvarcharmap = varcharvarcharmap + {'Vitrum edere possum, mihi non nocet.':'Vitrum edere possum, mihi non nocet.'} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varcharvarcharmap['Vitrum edere possum, mihi non nocet.'] = '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜' WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

INSERT INTO varcharmaptable (varcharkey, varcharvarintmap ) VALUES      ('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',  {' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑': -40,'Можам да јадам стакло, а не ме штета.': 110230,'I can eat glass and it does not hurt me': 1400} );

UPDATE varcharmaptable SET varcharvarintmap = varcharvarintmap + {'Vitrum edere possum, mihi non nocet.':20000} WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';

UPDATE varcharmaptable SET varcharvarintmap['Vitrum edere possum, mihi non nocet.'] = 1010010101020400204143243 WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜'
        """.encode("utf-8"))

        cursor = self.patient_cql_connection(node1).cursor()
        def verify_varcharmap(map_name, expected, encode_value=False):
            cursor.execute((u"SELECT %s FROM testks.varcharmaptable WHERE varcharkey= '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜';" % map_name).encode("utf-8"))
            if encode_value:
                got = {k.encode("utf-8"):v.encode("utf-8") for k,v in cursor.fetchone()[0].iteritems()}
            else:
                got = {k.encode("utf-8"):v for k,v in cursor.fetchone()[0].iteritems()}
            self.assertEqual(got, expected)

        verify_varcharmap('varcharasciimap', {
            'Vitrum edere possum, mihi non nocet.' : 'Hello',
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : 'My',
            'Можам да јадам стакло, а не ме штета.' : 'Name',
            'I can eat glass and it does not hurt me' : 'Is'
        })

        verify_varcharmap('varcharbigintmap', {
            'Vitrum edere possum, mihi non nocet.' : 5100003,
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : -45,
            'Можам да јадам стакло, а не ме штета.' : 12300,
            'I can eat glass and it does not hurt me' : 0
        })

        verify_varcharmap('varcharblobmap', {
            'Vitrum edere possum, mihi non nocet.' : binascii.a2b_hex("FEED103A"),
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : binascii.a2b_hex("DEADBEEF"),
            'Можам да јадам стакло, а не ме штета.' : binascii.a2b_hex("BEEFBEEF"),
            'I can eat glass and it does not hurt me' : binascii.a2b_hex("FEEB")
        })


        verify_varcharmap('varcharbooleanmap', {
            'Vitrum edere possum, mihi non nocet.' : True,
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : False,
            'Можам да јадам стакло, а не ме штета.' : False,
            'I can eat glass and it does not hurt me' : False
        })

        verify_varcharmap('varchardecimalmap', {
            'Vitrum edere possum, mihi non nocet.' : Decimal('50'),
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : Decimal('-20.4'),
            'Можам да јадам стакло, а не ме штета.' : Decimal('11234234.3'),
            'I can eat glass and it does not hurt me' : Decimal('10.0')
        })

        verify_varcharmap('varchardoublemap', {
            'Vitrum edere possum, mihi non nocet.' : 4234243,
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : -432.311,
            'Можам да јадам стакло, а не ме штета.' : 3.1415,
            'I can eat glass and it does not hurt me' : 20000.0
        })

        verify_varcharmap('varcharfloatmap', {
            'Vitrum edere possum, mihi non nocet.' : 10.0,
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : -234.3000030517578,
            'Можам да јадам стакло, а не ме штета.' : -234234,
            'I can eat glass and it does not hurt me' : 1000.5
        })

        verify_varcharmap('varcharintmap', {
            'Vitrum edere possum, mihi non nocet.' : 1,
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : 2,
            'Можам да јадам стакло, а не ме штета.' : -3,
            'I can eat glass and it does not hurt me' : -500
        })

        verify_varcharmap('varcharinetmap', {
            'Vitrum edere possum, mihi non nocet.' : '192.168.0.1',
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : '127.0.0.1',
            'Можам да јадам стакло, а не ме штета.' : '8.8.8.8',
            'I can eat glass and it does not hurt me' : '8.8.4.4'
        })

        verify_varcharmap('varchartextmap', {
            'Vitrum edere possum, mihi non nocet.' : 'Once I went',
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : 'On a trip',
            'Можам да јадам стакло, а не ме штета.' : 'Across',
            'I can eat glass and it does not hurt me' : 'The '
        })

        verify_varcharmap('varchartimestampmap', {
            'Vitrum edere possum, mihi non nocet.' : '\x00\x00\x01?Zs\x1dH',
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : '\x00\x00\x00r\x86\xfa\xe3\xc8',
            'Можам да јадам стакло, а не ме штета.' : '\x00\x00\x00\xdcj\xe1\xffh',
            'I can eat glass and it does not hurt me' : '\xff\xff\xff3\xa9\x0f^H'
        })

        verify_varcharmap('varcharuuidmap', {
            'Vitrum edere possum, mihi non nocet.' : UUID('7787064c-ce54-4324-abdd-05775b89ead7'),
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : UUID('1df0b6ac-f3d3-456c-8b78-2bc70e585107'),
            'Можам да јадам стакло, а не ме штета.' : UUID('e2ed2164-31dc-42cb-8ee9-47376e071210'),
            'I can eat glass and it does not hurt me' : UUID('a487fe45-8af5-4454-ac66-2614286d7e89')
        })

        verify_varcharmap('varchartimeuuidmap', {
            'Vitrum edere possum, mihi non nocet.' : UUID('4a36c100-d8ec-11e2-a28f-0800200c9a66'),
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : UUID('670c7f90-d8ec-11e2-a28f-0800200c9a66'),
            'Можам да јадам стакло, а не ме штета.' : UUID('750c2d70-d8ec-11e2-a28f-0800200c9a66'),
            'I can eat glass and it does not hurt me' : UUID('80d74810-d8ec-11e2-a28f-0800200c9a66')
        })

        verify_varcharmap('varcharvarcharmap', {
            'Vitrum edere possum, mihi non nocet.' : '᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜',
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑',
            'Можам да јадам стакло, а не ме штета.' : 'Можам да јадам стакло, а не ме штета.',
            'I can eat glass and it does not hurt me' : 'I can eat glass and it does not hurt me'
        }, encode_value=True)

        verify_varcharmap('varcharvarintmap', {
            'Vitrum edere possum, mihi non nocet.' : 1010010101020400204143243,
            ' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑' : -40,
            'Можам да јадам стакло, а не ме штета.' : 110230,
            'I can eat glass and it does not hurt me' : 1400
        })

        output = run_cqlsh(node1, 'use testks; SELECT * FROM varcharmaptable')

        self.assertEquals(output.count('Можам да јадам стакло, а не ме штета.'), 16)
        self.assertEquals(output.count(' ⠊⠀⠉⠁⠝⠀⠑⠁⠞⠀⠛⠇⠁⠎⠎⠀⠁⠝⠙⠀⠊⠞⠀⠙⠕⠑⠎⠝⠞⠀⠓⠥⠗⠞⠀⠍⠑'), 16)
        self.assertEquals(output.count('᚛᚛ᚉᚑᚅᚔᚉᚉᚔᚋ ᚔᚈᚔ ᚍᚂᚐᚅᚑ ᚅᚔᚋᚌᚓᚅᚐ᚜'), 2)


def run_cqlsh(node, cmds, cqlsh_options=[]):
    cdir = node.get_cassandra_dir()
    cli = os.path.join(cdir, 'bin', 'cqlsh')
    env = common.make_cassandra_env(cdir, node.get_path())
    host = node.network_interfaces['binary'][0]
    port = node.network_interfaces['binary'][1]
    args = cqlsh_options + [ host, str(port) ]
    sys.stdout.flush()
    p = subprocess.Popen([ cli ] + args, env=env, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    for cmd in cmds.split(';'):
        p.stdin.write(cmd + ';\n')
    p.stdin.write("quit;\n")
    p.wait()
    return p.stdout.read()
