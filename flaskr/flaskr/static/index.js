function number(x) {
if (x==1) return "one"; if (x==2) return "two"; if (x==3) return "three";
if (x==4) return "four"; if (x==5) return "five"; if (x==6) return "six";
if (x==7) return "seven"; if (x==8) return "eight"; if (x==9) return "nine";
if (x==10) return "ten"; if (x==11) return "eleven"; if (x==12) return "twelve";
return x; //default
}
function ishtime(h,m) {
h = number(h)
if (m<=3 || m>57) return h+" o'clock";
if (m<=7)  return "five past "+h;
if (m<=12) return "ten past "+h;
if (m<=17) return "quarter past "+h;
if (m<=23) return "twenty past "+h;
if (m<=28) return "twenty-five past "+h;
if (m<=33) return "half past "+h;
if (m<=38) return "twenty-five to "+h;
if (m<=43) return "twenty to "+h;
if (m<=48) return "quarter to "+h;
if (m<=53) return "ten to "+h;
if (m<=58) return "five to "+h;
return "h:m"; // never reached?
}
function daytime(h) {
if (!h || h>21) return " at night"
if (h<12) return " in the morning";
if (h<=17) return " in the afternoon";
return " in the evening"; // default
}
function ish(h,m) {
if (!h && !m) { // if no time supplied, use the system time
time = new Date()
h = time.getHours()
m = time.getMinutes()
}
z = daytime(h);
h = h % 12 // fix to 12 hour clock
if (m>57 && time.getSeconds()>30) m++; // round seconds
if (m>60) m=0 // round up minutes
if (m>33) h++ // round up hours
if (h>12)  h = 1 // the clock turns round..
if (h==0) h = 12
return "It's now about "+ishtime(h,m)+z+"."
}
ish()
