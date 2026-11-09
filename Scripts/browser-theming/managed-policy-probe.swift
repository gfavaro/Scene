import Foundation
// Prints the forced BrowserThemeColor for net.imput.helium whenever it changes. See docs/browser-theming.md.
setvbuf(stdout, nil, _IONBF, 0)
let app = "net.imput.helium" as CFString
var last = ""
Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
  CFPreferencesAppSynchronize(app)
  let v = "\(CFPreferencesCopyAppValue("BrowserThemeColor" as CFString, app) as Any) forced=\(CFPreferencesAppValueIsForced("BrowserThemeColor" as CFString, app))"
  if v != last { print(Date(), v); last = v }
}
RunLoop.main.run()
