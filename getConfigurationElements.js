//get category
var category = Server.getConfigurationElementCategoryWithPath(categoryPath);

//die in a fire if non-existent
if (category == null) {
	throw "Configuration element category '" + categoryPath + "' not found or empty!";
}

//get _all_ the elements
var elements = category.configurationElements;
var result = [];

//retrieve names
for (i = 0; i < elements.length; i++) {
	System.log("Found configuration element '" + elements[i].name + "'");
	result.push(elements[i].name);
}
//return results
return result
