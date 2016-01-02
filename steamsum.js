var get_num = function(str) {
  matches = str.match(/[\d\.]/g)
  if (matches) {
    return parseFloat(matches.join(''));
  }
  else {
    return null;
  }
}


var calc_diff = function(total) {
  var sign = 1;
  var value = 0;

  if (total.children.length) {
    var num_children = total.children.length;
    for (var i = 0; i < num_children; ++i) {
      var child = total.children[i];
      if (
        child.getAttribute('class') === 'wth_payment' &&
        child.innerHTML.toLowerCase().indexOf('credit') !== -1
      ) {
          sign = -1;
      }
      else if (child.attributes.length === 0) {
        value = get_num(child.innerHTML);
        console.log("credit " + value)
      }
    }
  }

  else {
    value = get_num(total.innerHTML)
    console.log("spend " + value)
  }
  return sign * value;
}

var sum_totals = function (totals)
{
  var credit = 0;
  var spent = 0;
  for (var i = 0; i < totals.length; ++i)
  {
    var diff = calc_diff(totals[i]);
    if (!diff) {
      continue;
    }
    if (diff < 0) {
      credit += -diff;
    }
    else {
      spent += diff;
    }
  }

  credit = '$' + credit.toFixed(2);
  spent = '$' + spent.toFixed(2);
  return {'credit': credit, 'spent': spent};
}


var totals = document.getElementsByClassName('wht_total ');
var result = sum_totals(totals);

alert('You\'ve spent ' + result['spent'] + ' and gained ' + result['credit']);
