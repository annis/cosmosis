import collections

enum_names = [
"DBS_SUCCESS",
"DBS_DATABLOCK_NULL",
"DBS_SECTION_NULL",
"DBS_SECTION_NOT_FOUND",
"DBS_NAME_NULL",
"DBS_NAME_NOT_FOUND",
"DBS_NAME_ALREADY_EXISTS",
"DBS_VALUE_NULL",
"DBS_WRONG_VALUE_TYPE",
"DBS_MEMORY_ALLOC_FAILURE",
"DBS_SIZE_NULL",
"DBS_SIZE_NEGATIVE",
"DBS_SIZE_INSUFFICIENT",
"DBS_LOGIC_ERROR",
]


class EnumGenerator(object):
	"""This is a slightly insane hack to generate an enum into the local
	namespace from a list of names.  This avoids a nested namespace.
	Once the list of errors has settled down so we do not need to keep
	retyping we can just hard-code them.
	"""
	def __init__(self, namespace):
		self.namespace=namespace
		self.value = 0
	def add(self, name):
		self.namespace[name] = self.value
		self.value += 1

enum = EnumGenerator(locals())
for name in enum_names:
	enum.add(name)

ERROR_MESSAGES = collections.defaultdict(lambda:  "{status}: Uknown error; possibly cosmosis internal failure.  Please contact cosmosis team")
ERROR_MESSAGES.update({
	DBS_DATABLOCK_NULL: "{status}: Null (zero) datablock passed into function (section was {section}, name was {name})",
	DBS_SECTION_NULL: "{status}: Null name passed into function (section was {section}",
	DBS_SECTION_NOT_FOUND: "{status}: Could not find section called {section} (name was {name})",
	DBS_NAME_NULL: "{status}: Null name passed into function (section was {section})",
	DBS_NAME_NOT_FOUND: "{status}: Could not find name {name} in section {section}",
	DBS_NAME_ALREADY_EXISTS: "{status}: Tried to overwrite {name} in section {section}.  Use the replace functions to over-write",
	DBS_VALUE_NULL: "{status}: Passed a null value into function (section was {section}, name was {name})",
	DBS_WRONG_VALUE_TYPE: "{status}: Tried to overwrite {name} in section {section} with a value of the wrong type",
	DBS_MEMORY_ALLOC_FAILURE: "{status}: Failed to allocate memory for {name} in section {section}.",
	DBS_SIZE_NULL: "{status}: Null parameter for returned size passed into function (section was {section}, name was {name})",
	DBS_SIZE_NEGATIVE: "{status}: Negative maximum size passed into function (section was {section}, name was {name}",
	DBS_SIZE_INSUFFICIENT: "{status}: Size of passed in array not large enough for what is needed (section was {section}, name was {name}",
	DBS_LOGIC_ERROR: "{status}: Internal cosmosis logical error.  Please contact cosmosis team (section was {section}, name was {name})",
})

class BlockError(Exception):
	def __init__(self, status, section, name):
		self.name=name
		self.status=status
		self.section=section
	def __str__(self):
		return ERROR_MESSAGES[self.status].format(status=self.status, name=self.name,section=self.section)


