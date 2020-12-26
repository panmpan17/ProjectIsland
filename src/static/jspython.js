// 
// Integer Extension
// 

int = parseInt;

// 
// String Extension
// 

String.prototype.find = String.prototype.indexOf;
String.prototype.format = function () {
    var args = arguments;
    var newText = this;
    for (var i = 0; i < args.length; i++) {
        if (newText.indexOf("{}") != -1) {
            newText = newText.replace("{}", args[i]);
        }
    }

    return newText;
};
String.prototype.replaceMap = function (map) {
    var result = this;
    for (var key in map) {
        result = result.replace(key, map[key]);
    }
    return result;
};
str = String;

// 
// Array Extension
// 

Array.prototype.index = Array.prototype.indexOf;
Array.prototype.append = Array.prototype.push;
Array.prototype.remove = function (ele, num) {
    num = num == undefined ? 1 : num;
    if (num <= 0) {
        throw "The number of element remove need to be bigger than 0";
    }

    var find = this.index(ele);
    var removed = 0;
    while (find >= 0 && (removed < num || num == -1)) {
        this.splice(find, 1);
        find = this.index(ele);
        removed += 1;
    }
};

Array.prototype.count = function (ele) {
    var count = 0;
    for (var i = 0; i < this.length; i++) {
        if (this[i] == ele) {
            count += 1;
        }
    }

    return count;
};

Array.prototype.pop = function (index) {
    index = index == undefined ? (this.length - 1) : index;
    if (this[index] == undefined) {
        index = (this.length - 1);
        // throw "Index must not bigger than list length";
    }

    return this.splice(index, 1)[0];
};

Array.prototype.insert = function (index, ele) {
    if (index == undefined || ele == undefined) {
        throw "Missing argument";
    }

    this.splice(index, 0, ele);
};

Array.prototype.copy = function () {
    return this.slice();
};

//
// Dictionary
//
function Copy(dict) {
    var d = {};
    for (var key in dict)
        d[key] = dict[key]
    return d;
}


// 
// Random Module
// 

var Random = function () {
    var self = this;

    this.randint = function (start_num, end_num) {
        return int(Math.random() * (end_num - start_num + 1) + start_num);
    }

    this.random = function () {
        return Math.random();
    }

    this.shuffle = function (list) {
        var j, x, i;
        for (i = list.length - 1; i > 0; i--) {
            j = Math.floor(Math.random() * (i + 1));
            x = list[i];
            list[i] = list[j];
            list[j] = x;
        }
    }

    this.choice = function (list) {
        return list[self.randint(0, list.length - 1)];
    }

    this.sample = function (list, num) {
        if (num > list.length) {
            throw "Sample larger than population";
        }

        var picks = [];

        for (i = 0; i < num; i++) {
            pick = self.choice(list);

            while (picks.index(pick) >= 0) {
                pick = self.choice(list);
            }

            picks.push(pick);
        }

        return picks;
    }
};

random = new Random();

// For loop
foreach = function (iterate_object, iterate_function) {
    keys = Object.keys(iterate_object);
    for (i = 0; i < keys.length; i++) {
        iterate_function(keys[i], iterate_object[keys[i]]);
    }
};

// Date
Date.prototype.strftime = function (format) {
    str = format.replace("%Y", this.getFullYear());
    var month = (this.getMonth() + 1).toString();
    if (month.length == 1)
        month = "0" + month;
    str = str.replace("%m", month);

    var date = this.getDate().toString();
    if (date.length == 1)
        date = "0" + date;
    str = str.replace("%d", date);

    var hours = this.getHours().toString();
    if (hours.length == 1)
        hours = "0" + hours;
    str = str.replace("%H", hours);

    var mintues = this.getMinutes().toString();
    if (mintues.length == 1)
        mintues = "0" + mintues;
    str = str.replace("%M", mintues);

    var seconds = this.getSeconds().toString();
    if (seconds.length == 1)
        seconds = "0" + seconds;
    str = str.replace("%S", seconds);
    return str;
};

var DateKeyword = [
    "Y",
    "m",
    "d",
    "H",
    "M",
    "S",
]

Date.strptime = function (format, string) {
    var fragments = [];
    var scanKeyword = false;
    for (var letter of format) {
        if (letter == "%") scanKeyword = true;
        else if (scanKeyword) {
            if (DateKeyword.includes(letter)) {
                scanKeyword = false;
                fragments.push("%" + letter);
            }
            else
                throw new Error(`Fromat parse failed: '${letter}'`);
        }
        else {
            if (fragments[fragments.length - 1].startsWith("%"))
                fragments.push(letter);
            else
                fragments[fragments.length - 1] = fragments[fragments.length - 1] + letter;
        }
    }

    var startIndex = 0;
    var data = {};
    for (var i = 0; i < fragments.length; i++) {
        var fragment = fragments[i];
        if (fragment.startsWith("%")) {
            var endIndex = string.length;
            if ((i + 1) < fragments.length) endIndex = string.indexOf(fragments[i + 1], startIndex);

            var value = int(string.substring(startIndex, endIndex));
            if (isNaN(value))
                throw new Error(`String to int failed: '${value}'`);

            data[fragment.substring(1)] = value;

            if ((i + 1) < fragments.length) startIndex = endIndex + fragments[i + 1].length;
        }
    }

    var date = new Date(year = 0, month = 0, date = 1, hours = 0, minutes = 0, seconds = 0, ms = 0);
    if (data["Y"]) date.setYear(data["Y"]);
    if (data["m"]) date.setMonth(data["m"] - 1);
    if (data["d"]) date.setDate(data["d"]);

    if (data["H"]) date.setHours(data["H"]);
    if (data["M"]) date.setMinutes(data["M"]);
    if (data["S"]) date.setSeconds(data["S"]);

    return date;
};