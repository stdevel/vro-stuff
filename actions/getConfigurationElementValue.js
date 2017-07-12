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
	if (elements[i].name == elementName) {
		//found required element
		var attribute = elements[i].getAttributeWithKey(attributeName);
		if (attribute != null) {
			System.log("Found attribute '" + attributeName + "' in '" + elementName + "' with value '" + attribute.value + "'");
			return attribute.value;
		}
		else {
			throw "Attribute '" + attributeName + "' not found!";
		}
	}
}
