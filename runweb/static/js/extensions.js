/**
 * @namespace
 * @name extensions
 */

/**
 * Extends jQuery with a function to get the absolute offset of an element on a page.
 * @example
 * // returns {left: 0, top: 0}
 * $('body').getOffset();
 * @memberof extensions
 * @param {String} [attribute] The part of the offset to get. Can be "left" or "top". Leave unset or use null to get the full offset.
 * @returns {Number|Object} The number corresponding to the requested attribute. If no specific attribute was requested, an object with the full offset.
 */
jQuery.fn.getOffset = function(attribute)
{
	var result = {left: 0, top: 0};
	var element = $(this)[0];
	
	do
	{
		// Recursively add the offset of each element until there are no more ancestors
		result.left += element.offsetLeft;
		result.top += element.offsetTop;
		element = element.offsetParent;
	}
	while (element);
	
	// If a specific attribute was requested, return that one only
	if (attribute)
	{
		if (result[attribute])
			return result[attribute];
		else
			throw '"' + attribute.toString() + '" is not a valid offset attribute. Use "left", "top", or nothing.'
	}
	
	return result;
}