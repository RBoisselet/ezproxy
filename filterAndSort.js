function makeList(selector) {
	var nodeList = [].slice.call(document.querySelectorAll(selector));
  var list = []
  nodeList.forEach( function(element) {
    text = element.innerText;
    url = element.href;
    link = [text, url];
    list.push(link);
  });
  return list
}


function sortList(list, direction) {
	if (direction == "az") {
		sorted_list = list.sort(function (a, z) {
			return a[0].localeCompare(z[0]);
		});
	}
	else if (direction == "za") {
			sorted_list = list.sort(function (a, z) {
			return z[0].localeCompare(a[0]);
		});
	}
	else {
		console.log('Error: a sorting direction must be set (az or za) in second argument')
		return
	}
  return sorted_list
}


function alterTable(selector, sorted_list) {
	links = document.querySelectorAll(selector);
	links.forEach( function(link, i) {
  	link.href = sorted_list[i][1];
  	link.innerText = sorted_list[i][0];

	});
}

function checkInput(element) {
  return element[0].toLowerCase().indexOf(input.value.toLowerCase()) >= 0;
}

function mark(selector) {

  links_to_mark = document.querySelectorAll(selector);
  links_to_mark.forEach( function(link_to_mark) {
    var inputText = link_to_mark;
    var innerHTML = inputText.innerHTML;
    
    innerHTML = innerHTML.replace('<mark>','').replace('</mark>','');
    inputText.innerHTML = innerHTML;
    
    var index = innerHTML.toLowerCase().indexOf(input.value.toLowerCase());

    if (index >= 0 && input.value.length > 0) { 
      innerHTML = innerHTML.substring(0,index) + "<mark>" + innerHTML.substring(index,index+input.value.length) + "</mark>" + innerHTML.substring(index + input.value.length);
      inputText.innerHTML = innerHTML;
    }   
  });
}

function updateTable(newList) {

  // Replace the display table by the sorted list
  var display_table = document.querySelector('#display_table tbody');
  display_table.innerHTML = '';

    newList.forEach( function(new_link, i) {
    // Create a tr element with a td and a elements inside
    var new_tr = document.createElement('tr');
    var new_td = document.createElement('td');
    new_td.classList.add('domain');
    var new_a = document.createElement('a');
    new_a.classList.add('database-link');
    new_a.href = new_link[1]
    new_a.innerText = new_link[0]
    new_a.target = '_blank';
    new_td.appendChild(new_a);
    new_tr.appendChild(new_td);
    display_table.appendChild(new_tr);
  });
}

function sort(option) {
// Make a list of <a> elements : [[title, url]]
  list = makeList('.domain a');
  
  // Get the sorting button class and infer sorting order
  direction = document.getElementById('sorting-icon');
  
  if (option == 'regular') {

    if (direction.classList.contains('glyphicon-sort-by-alphabet') == true) {
      sorted_list = sortList(list, 'az');
      direction.classList.remove('glyphicon-sort-by-alphabet');
      direction.classList.add('glyphicon-sort-by-alphabet-alt');
    } else if (direction.classList.contains('glyphicon-sort-by-alphabet-alt') == true) {
      sorted_list = sortList(list, 'za');
      direction.classList.remove('glyphicon-sort-by-alphabet-alt');
      direction.classList.add('glyphicon-sort-by-alphabet');
    } else {}

  } else if (option == 'reverse') {

    if (direction.classList.contains('glyphicon-sort-by-alphabet') == true) {
      sorted_list = sortList(list, 'za');
      direction.classList.remove('glyphicon-sort-by-alphabet-alt');
      direction.classList.add('glyphicon-sort-by-alphabet');
    } else if (direction.classList.contains('glyphicon-sort-by-alphabet-alt') == true) {
      sorted_list = sortList(list, 'az');
      direction.classList.remove('glyphicon-sort-by-alphabet');
      direction.classList.add('glyphicon-sort-by-alphabet-alt');
    } else {}

  }

  else {}

  return sorted_list;
}

// Create the initial link list
document.addEventListener("DOMContentLoaded", function(event) { 
  constant_list = makeList('.domain a');
});

// Sorting event: on click, sort, alter the table and replace the
// sorting button by the oppisite order : a-z => z-a ; z-a => a-z

document.getElementById('sorting').addEventListener("click", function() {
	
  
  sorted_list = sort('regular');

  updateTable(sorted_list);
  //alterTable('.domain a', sorted_list);

  mark('.domain a');
  
});


input = document.getElementById('db_search');

// Event on input keyup: filter the table and mark the matching string in the
// filtered list

input.addEventListener('keyup', function(e) {
  
  // Fetch the initial link list
  var links_unfiltered = constant_list;
  
  // Filter the list by input (see checkInput callback function)
  links_filtered = links_unfiltered.filter(checkInput);
  
  updateTable(links_filtered);

  sorted_list = sort('reverse');

  updateTable(sorted_list);
  

  // Highlight matching strings in the filtered list
  mark('.domain a');
  
});
