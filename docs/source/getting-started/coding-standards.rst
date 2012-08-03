
Kódolási irányelvek
###################

Ennek az oldalnak a célja, hogy bemutassa az általam lefektetett kódolási irányelveket, amelyeket a kód teljes egészében alkalmazok.


Verziók
*******
.. warning:: A kód az 1.Y verzió eléréséig beta állapotban van, ami annyit takar, hogy az egyes kiadásokban is lehetnek nagyobb különbségek.

 
Az xadrpy kiadásai során az alábbi konvenciókat követem.

X
	Fő verzió (például (0.Y, 1.Y) - a különböző fő verziók egymáshoz képest átfogó különbségeket is tartalmazhatnak.
	
X.Y
	Verzió (például 0.4, 1.0) - Az egyes verziók egymáshoz képest nagyobb mérvű átalakításokat is tartalmazhatnak, de szerkezetileg egymásra épül. 

X.Y.Z
	Release - kiadás.
	
	Egyesmáshoz képes nem tartalmaz függőségeket, nem módosul az adatbázis felépítés.


Appok elhelyezkedése
********************

.. note:: `django` terminológia szerint az egyes önálló egységek neve: application (app). 

Az alap csomag az `xadrpy`, ez alatt találhatóak az egyes fő app-ok (core).
Ilyen core app például az `api`, `workers`, stb.

.. note:: Néhány kiegészítő funkció miatt az `xadrpy` funkcionál mint app. 

A kiegészítő appok például a `contrib` illetve a `social` alatt találhatóak.

A `vendor` alatt azon az `xadrpy` részeként használható appok, csomagok találhatóak, 
amelyek legfeljebb minimális módosítással kerültek be a keretrendszerbe, vagy csak arra építkezik.

Egyes appok felépítése
**********************

Modulok
=======
* `__init__.py` - publikus interface
* `defaults.py` - Alapértékek 
* `conf.py` - Csomag beállításai, alapértékei
* `base.py` - Alap funkciók, a csomag tetszőleges része importálhatja
* `managers.py` - *adatelérési réteg (DAL)*
* `models.py` - adatbázis modellek 
* `libs.py` - *Üzleti logika (BLL)*
* `urls.py` - URL felépítés
* `admin.py` - `django admin` felülethez interface
* `views.py` - view függvények, osztályok
* `xtensions.py` - `xadrpy` kiterjesztések
* `middleware.py` - Request middleware osztályok
* `signals.py` - Publikus szignálok
* `context_processors.py` - Template context kiterjesztések

Csomagok
========
* `templatetags` - az app által publikált template tag-ek
* `migrations` - Adatbázis migrációk
* `management.commands` - A csomag által publikált django-admin parnacsok
		
Almappák
========
* `templates` - A csomag template fájljai
* `static` - A csomag 


.. note:: Az egyes modulok opcionálisak, nem feltétlen implementálja minden csomag.
.. note:: A felépítés tervezésekor figyelembe vettem a `django` irányelveit.
