#1 Versions
===========

Changeset model
---------------

.. code-block:: python

	class ChangeSet(MPTTModel):
		parent = TreeForeginKey('self', blank=True, null=True, verbose_name="subversions")
		obj_id = models.IntegerField()
		obj_ct = models.ForeginKey(ContentType)
		obj = GenericForeignKey('obj_id', 'obj_ct')
		version = models.CharField(max_length=255)	#???
		created = models.DateTimeField(auto_now_add=True)
		user = models.ForeginKey(User)
		group = models.ForeginKey(Group)	#???
		comment = models.ChatField(max_length=255, blank=True, null=True)
		values = DictField()
		
