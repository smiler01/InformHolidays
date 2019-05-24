var addZeroPadding = n => {
  return ("0" + n).slice(-2);
};

var getTodayString = () => {
  var date = new Date();
  var year = date.getFullYear();
  var month = addZeroPadding(date.getMonth() + 1);
  var day = addZeroPadding(date.getDate());
  var week = Array(
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
  )[date.getDay()];
  var todayString = year + "/" + month + "/" + day;
  document.getElementById("today-date-content").innerHTML =
    todayString + " " + week;
  return todayString;
};
getTodayString();

var getHolidayDatelist = () => {
  var req = new XMLHttpRequest();
  req.open("get", "../static/data/syukujitsu_linux.csv", true);
  req.send(null);
  req.onload = () => {
    //printHolidayDate(req.responseText);
    getNextConsectiveHoliday(req.responseText);
  };
};

var purgeHolidayDateList = str => {
  // 祝日データベースからタイムスタンプと祝日名を取得
  var holidayList = [];
  var holidayTimestamp = null;
  var holidayName = null;
  str.split("\n").forEach(x => {
    holidayTimestamp = Date.parse(x.split(",")[0]);
    holidayName = x.split(",")[1];
    holidayList.push({
      timestamp: holidayTimestamp,
      name: holidayName,
      type: "public"
    });
  });
  holidayList.shift(); // ヘッダ要素（先頭）を削除
  holidayList.pop(); // 無駄な空行列があるため最終要素を削除

  // 祝日データベースの先頭と最後尾のタイムスタンプの間に含まれる全日数を取得
  const firstTimestamp = holidayList[0].timestamp;
  const lastTimestamp = holidayList[holidayList.length - 2].timestamp;
  const diffDay = (lastTimestamp - firstTimestamp) / (1000 * 60 * 60 * 24);

  // 全日数間から土日を抜き出す
  var holidayDate = null;
  const dayOfWeekStr = ["日", "月", "火", "水", "木", "金", "土"];
  for (var i = 0; i < diffDay; i++) {
    holidayTimestamp = firstTimestamp + i * (1000 * 60 * 60 * 24);
    holidayDate = new Date(holidayTimestamp);
    // 土日のみを抽出
    if (holidayDate.getDay() === 0 || holidayDate.getDay() === 6) {
      holidayList.push({
        timestamp: holidayTimestamp,
        name: dayOfWeekStr[holidayDate.getDay()],
        type: "normal"
      });
    }
  }

  // 連想配列をtimestamp順にソート
  holidayList.sort((a, b) => {
    if (a.timestamp < b.timestamp) return -1;
    if (a.timestamp > b.timestamp) return 1;
    return 0;
  });

  // 重複要素を削除
  for (var i = 1; i < holidayList.length; i++) {
    if (holidayList[i].timestamp === holidayList[i - 1].timestamp) {
      if (holidayList[i].type === "normal") {
        holidayList.splice(i, 1);
      }
    }
  }

  return holidayList;
};

var getNextConsectiveHoliday = str => {
  var holidaylist = purgeHolidayDateList(str);
  var todayTimestamp = Date.parse(getTodayString());
  var targetTimestamp;
  var tomorrowList = [];
  holidaylist.forEach(x => {
    targetTimestamp = x.timestamp;
    if (targetTimestamp >= todayTimestamp) {
      tomorrowList.push(x);
      console.log(x.timestamp, x.name);
    }
  });
  //
  var parseConsecutiveHolydayList = [];
  var tmplist = [];
  for (var i = 0; i < tomorrowList.length - 1; i++) {
    preTomorrowDate = new Date(tomorrowList[i].timestamp);
    preTomorrowWeeknumber = preTomorrowDate.getDay();
    curTomorrowDate = new Date(tomorrowList[i + 1].timestamp);
    curTomorrowWeeknumber = curTomorrowDate.getDay();
    if (preTomorrowWeeknumber === 6 && curTomorrowWeeknumber === 0) {
      preTomorrowWeeknumber = -1;
    }
    if (preTomorrowWeeknumber + 1 === curTomorrowWeeknumber) {
      tmplist.push(tomorrowList[i]);
    } else {
      if (tmplist.length > 2) parseConsecutiveHolydayList.push(tmplist);
      tmplist = [];
    }
  }
  //
  parseConsecutiveHolydayList.forEach(ConsecutiveList => {
    ConsecutiveList.forEach(x => {
      var tmpDate = new Date(x.timestamp);
      var string =
        tmpDate.getFullYear() +
        "/" +
        (tmpDate.getMonth() + 1) +
        "/" +
        tmpDate.getDate();
      console.log(string, x.timestamp, x.name, x.type);
    });
  });
};

getHolidayDatelist();

var printHolidayDate = str => {
  var date = purgeHolidayDateList(str);
  var inner;
  date.forEach(x => {
    inner += `<p>${x[0]} ${x[1]}</p>`;
  });
  holidayElement.innerHTML = inner;
};

setInterval("getTodayString", 1000);
