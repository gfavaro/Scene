import Foundation
// Usage: sudo managed-policy-write <user> <bundle-id> <key> <string-value>. An empty value removes the key.
// Writes the managed plist directly, then tells cfprefsd and its clients that the domain changed.
let a = CommandLine.arguments
guard a.count == 5 else { print("usage: managed-policy-write user bundle-id key value"); exit(2) }
let (user, domain, key, value) = (a[1], a[2], a[3], a[4])
let h = dlopen("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation", RTLD_NOW)
typealias Changed = @convention(c) (CFArray) -> Void
let changed = unsafeBitCast(dlsym(h, "_CFPreferencesManagementStatusChangedForDomains")!, to: Changed.self)
let path = "/Library/Managed Preferences/\(user)/\(domain).plist"
let dict = NSMutableDictionary(contentsOfFile: path) ?? NSMutableDictionary()
if value.isEmpty { dict.removeObject(forKey: key) } else { dict[key] = value }
var ok = true
if dict.count == 0 { ok = (try? FileManager.default.removeItem(atPath: path)) != nil }
else { ok = dict.write(toFile: path, atomically: true); chmod(path, 0o644) }
changed([domain] as CFArray)
print("write ok:", ok, "->", NSDictionary(contentsOfFile: path) ?? [:])
