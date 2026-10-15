# ⚠️ Legal & Ethical Disclaimer

**PhoneStalker** is released strictly for **educational purposes, authorized
security auditing, and lawful OSINT (Open-Source Intelligence) research and
training.**

## What this tool actually does

PhoneStalker is a thin, offline wrapper around Google's open-source
[`phonenumbers`](https://github.com/google/libphonenumber) library. All data
it displays comes from **publicly published telecom numbering-plan
metadata** bundled inside that library. Specifically, it can tell you:

- Whether a number is *structurally valid* for its country's numbering plan
- The number's E.164 / international / national formatting
- The general **line type category** (mobile, landline, VoIP, etc.) implied
  by the numbering plan
- The **carrier range** a number block was originally assigned to (this can
  be outdated if the number was ported to another carrier)
- The **geographic region** historically associated with that number prefix
- The **timezone(s)** associated with that region

## What this tool does NOT do

- ❌ It does **not** perform live/real-time geolocation of a device or person
- ❌ It does **not** reveal a subscriber's name, address, or identity
- ❌ It does **not** query any telecom, government, or third-party API
- ❌ It does **not** access call logs, messages, contacts, or social media
- ❌ It cannot track a phone's current physical location

Any claim, service, or fork of this project suggesting otherwise is
misrepresenting the underlying technology.

## Authorized Use Only

By downloading, installing, or using this software, you agree that:

1. You will only look up phone numbers that you **own**, or numbers you are
   **explicitly authorized** to analyze (e.g. as part of a sanctioned
   penetration test, fraud investigation, or OSINT training exercise with
   documented consent/authorization).
2. You will **not** use this tool to harass, stalk, intimidate, dox, or
   surveil any individual without their informed consent.
3. You are solely responsible for complying with all local, national, and
   international laws regarding telecommunications data, privacy, and
   computer use (including but not limited to GDPR, CCPA, and applicable
   computer-misuse / anti-stalking legislation in your jurisdiction).
4. The author(s) and contributors of this project **assume no liability**
   for misuse, damages, or legal consequences resulting from the use or
   misuse of this software.

## Reporting Misuse

If you become aware of this tool being used for harassment, stalking, or
any unlawful purpose, please report it to the appropriate local authorities
and, if applicable, to the platform hosting the offending fork or
distribution.

---

**Use responsibly. Consent and authorization are not optional.**
