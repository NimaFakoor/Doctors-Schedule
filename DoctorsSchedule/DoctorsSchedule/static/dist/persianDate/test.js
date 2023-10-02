var pDate = new persianDate();

/*en*/
console.group("%cen", "font-size:20px;background:red;padding:0px 5px;border-radius:5px")
console.log(pDate.toLocale('en').format()); // 1400-04-18 15:32:12 PM
console.log(pDate.toLocale("en").format("YYYY")); // 1400
console.log(pDate.toLocale("en").format("MM")); // 04
console.log(pDate.toLocale("en").format("DD")); // 18
console.log(pDate.toLocale("en").format("dddd")); // friday
console.log(pDate.toLocale("en").format("MMMM")); // tir
console.groupEnd()


/*fa*/
console.group("%cfa", "font-size:20px;background:red;padding:0px 5px;border-radius:5px")
console.log(pDate.toLocale('fa').format()); // ۱۴۰۰-۰۴-۱۸ ۱۵:۳۲:۳۲ ب ظ
console.log(pDate.toLocale("fa").format("YYYY")); // ۱۴۰۰
console.log(pDate.toLocale("fa").format("MM")); // ۰۴
console.log(pDate.toLocale("fa").format("DD")); // ۱۸
console.log(pDate.toLocale("fa").format("dddd")); // جمعه
console.log(pDate.toLocale("fa").format("MMMM")); // تیر
console.groupEnd()