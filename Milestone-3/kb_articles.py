# Enterprise IT Knowledge Base - 10 detailed articles
# Each 300-500 words, covering a distinct IT support scenario

articles = [
{
    "kb_id": 'KB-101',
    "title": 'VPN Troubleshooting Guide',
    "category": 'Networking',
    "tags": ['VPN', 'Remote Access'],
    "last_updated": '2026-07-15',
    "priority": 'Low',
    "version": '1.1',
    "author": 'Network Team',
    "content": """Overview
This guide covers common VPN connectivity issues faced by remote employees and how to resolve them without escalating to IT support. VPN reliability is critical for remote and hybrid staff, since it is often the only path to internal systems, shared drives, and internal applications while working outside the office. Most VPN problems fall into a small number of predictable categories, and the majority can be resolved by the employee directly within a few minutes using the steps below.

Symptoms
Users may experience the VPN client failing to connect entirely, repeated disconnections every few minutes even after a successful login, noticeably slow speeds while connected compared to the office network, or being unable to reach internal resources such as shared drives or internal websites despite the client showing a connected status. Some users also report the client hanging on a "negotiating security settings" screen indefinitely, or receiving certificate warnings that were not present previously.

Troubleshooting Steps
First, confirm your internet connection is stable by loading a website outside the VPN entirely, since a VPN cannot function properly on top of an already unstable connection. Next, restart the VPN client completely by closing it from the system tray rather than simply clicking reconnect, as a full restart clears cached session state that a simple reconnect does not. Check that your VPN client is on the latest version, as outdated clients frequently fail to negotiate security settings with newer gateway configurations. If you are on public WiFi, be aware that some networks actively block VPN ports; try switching to a mobile hotspot to confirm whether the network itself is the problem. Clear the VPN configuration cache and re-enter your credentials if the client shows a certificate error, since expired local certificates are a common and easily fixed cause. If you can connect but cannot reach internal resources, check whether split tunneling is enabled incorrectly, which can route internal traffic outside the tunnel by mistake.

Resolution
Most connectivity issues resolve after a full restart of the VPN client and confirming the latest version is installed, which together resolve the large majority of reported cases. If problems persist after completing all steps above, the issue is likely on the gateway side rather than your local machine, and should be escalated to network administration with the exact error message, a timestamp, and whether the issue is isolated to you or affects colleagues as well."""
},
{
    "kb_id": 'KB-102',
    "title": 'Resetting Your Network Password',
    "category": 'Password Reset',
    "tags": ['Password Reset', 'Account Lockout'],
    "last_updated": '2026-06-30',
    "priority": 'High',
    "version": '1.2',
    "author": 'Identity & Access Team',
    "content": """Overview
Employees are occasionally locked out of their accounts due to expired or forgotten passwords, and this is one of the most common support requests across the organization. This article explains the self-service reset process so most employees can resolve the issue themselves without waiting on a support ticket. Understanding why lockouts happen also helps prevent repeat occurrences.

Symptoms
You may see a message stating your password has expired and prompting an immediate change, or receive repeated login failures despite entering what you believe is the correct password. Some users also encounter a lockout message after several failed attempts, which is a security measure that temporarily disables the account rather than a sign of a technical fault. Occasionally, a password that worked yesterday stops working today with no message explaining why, which usually indicates a scheduled expiration.

Troubleshooting Steps
Navigate to the self-service password portal and select forgot password from the login screen. Enter your employee ID and the email address currently registered to your account, since using an old or personal email will cause the reset to fail silently. A reset link will typically be sent within a few minutes; check your spam or junk folder if it does not arrive, as corporate mail filters occasionally flag automated reset emails. When creating a new password, ensure it meets the complexity requirements: at least twelve characters, including one uppercase letter, one number, and one special character. Avoid reusing any of your last five passwords, as the system will silently reject repeats without always explaining why the new password was not accepted. If you are attempting this from a personal device rather than a company laptop, confirm you are on a network that can reach the reset portal, as some personal networks block corporate authentication traffic.

Resolution
Once reset, allow up to fifteen minutes for the new password to fully sync across all connected systems, including email, VPN, and internal applications, since propagation is not always instantaneous. Attempting to log in immediately after a reset before this window has passed is the most common reason a "successful" reset still appears to fail. If you remain locked out after this window has passed, contact IT support directly, as your account may require a manual unlock that cannot be completed through self-service."""
},
{
    "kb_id": 'KB-103',
    "title": 'Network Firewall Configuration',
    "category": 'Networking',
    "tags": ['Firewall', 'Network', 'Security'],
    "last_updated": '2026-07-01',
    "priority": 'Medium',
    "version": '1.3',
    "author": 'Network Team',
    "content": """Overview
This guide explains how firewall rules affect application connectivity and what to do when a required service is being blocked unexpectedly. Firewalls are a critical layer of network security, but they occasionally block legitimate business traffic, particularly after policy updates or when new tools are introduced without a corresponding exception request. Understanding this process helps employees resolve blocked-application issues faster and through the correct channel.

Symptoms
Applications may fail to connect to external services, show generic timeout errors with no further explanation, or be unable to reach certain internal servers while other network traffic continues to work normally. This selective failure pattern, where some services work and others do not, is usually a strong indicator of a firewall rule rather than a broader network outage. Some employees also notice that a tool worked fine yesterday and stopped working today with no local changes made, which typically points to a recent policy update.

Troubleshooting Steps
First identify which specific application and destination are affected, including the port number if it is known, since firewall exceptions are granted at this level of specificity rather than broadly. Check whether the issue is isolated to your machine or affects your entire team, which is an important distinguishing signal: a team-wide issue indicates a broader firewall rule change, while an isolated issue suggests a local misconfiguration or a machine-specific policy difference. Review any recent firewall policy announcements from network administration that may have changed default behavior, since teams are usually notified in advance of major changes. For internal tools specifically, confirm the tool's required ports against the current whitelist maintained by network administration, as internal tooling occasionally changes its required ports during updates without wide notice.

Resolution
If a legitimate business application is being blocked, submit a firewall exception request through the standard IT portal, including the application name, destination IP address or domain, the specific port number required, and a clear business justification for the access. Exception requests are typically reviewed within one to two business days depending on the sensitivity of the access requested. Temporary local firewall changes should never be made independently without formal approval, even as a short-term workaround, since unauthorized changes can expose the network to real security risk and are difficult to track during incident response."""
},
{
    "kb_id": 'KB-104',
    "title": 'Outlook Email Sync Issues',
    "category": 'Email',
    "tags": ['Email', 'Outlook', 'Sync'],
    "last_updated": '2026-07-10',
    "priority": 'Low',
    "version": '1.0',
    "author": 'Collaboration Tools Team',
    "content": """Overview
This article addresses common Outlook synchronization problems where new emails fail to appear, outgoing mail gets stuck, or the desktop and mobile experience fall out of sync with each other. Sync issues are among the most disruptive email problems since they are not always obvious until an important message is missed entirely, so it is worth understanding the common root causes.

Symptoms
Outlook may show as connected in the status bar but not display new incoming messages that have clearly already arrived based on notifications on other devices. Outgoing mail may get stuck in a permanent "sending" state that never resolves on its own. Some users notice a mismatch between the desktop application and the mobile app, where one shows messages the other does not, which usually points to a sync delay rather than a lost message. In more severe cases, Outlook may become unresponsive entirely when switching between folders.

Troubleshooting Steps
Restart Outlook completely rather than simply refreshing the inbox, since a soft refresh does not always clear a stuck sync process. Independently check your internet connection outside of Outlook to rule out a broader connectivity issue rather than an application-specific one. Verify your mailbox is not near its storage quota, since full or nearly full mailboxes can silently block new mail delivery without always displaying a clear warning message. If corruption is suspected, particularly after an unexpected shutdown or crash, the local Outlook data file may need to be rebuilt, which resolves persistent sync failures that survive a simple restart. Confirm your account credentials have not expired or require reauthentication, particularly if multi-factor authentication was recently enabled or reconfigured on your account, as this can silently break background sync until re-authenticated.

Resolution
Most sync issues resolve with a full application restart combined with a check of mailbox storage, which together account for the majority of reported cases. If the local data file is found to be corrupted, IT can provide a clean rebuild without losing any existing emails, provided the account is properly backed up first, which is standard practice before any data file operation. Persistent issues after these steps should be reported with the exact time the sync stopped working and any error codes displayed."""
},
{
    "kb_id": 'KB-105',
    "title": 'Laptop Overheating and Shutdown Issues',
    "category": 'Hardware',
    "tags": ['Hardware', 'Laptop', 'Overheating'],
    "last_updated": '2026-06-20',
    "priority": 'High',
    "version": '1.1',
    "author": 'Hardware Support Team',
    "content": """Overview
Laptops shutting down unexpectedly or feeling excessively hot during normal use are usually caused by a combination of dust buildup, excessive background processes, or a failing cooling component, and identifying which of these applies determines whether the fix is something you can do yourself or requires physical hardware service. Overheating left unaddressed can shorten the lifespan of internal components significantly.

Symptoms
The device may shut down without warning during intensive tasks such as video calls or large file operations, feel noticeably hot to the touch even during comparatively light use like document editing, or have a fan that runs constantly at high speed regardless of workload. Some users also notice a burning smell or unusual vibration, which should be treated as more urgent and reported immediately rather than troubleshot independently.

Troubleshooting Steps
Check for excessive background processes using the task manager, as runaway applications consuming high CPU are a common and easily overlooked cause of overheating that has nothing to do with the physical hardware. Ensure vents are not blocked by placing the laptop on a hard, flat surface rather than a bed, cushion, or lap, all of which restrict airflow significantly and are a surprisingly common root cause. If the device is more than two years old, physical dust buildup inside the fan assembly becomes increasingly likely and typically requires a professional cleaning rather than a software fix. Update to the latest firmware and BIOS version available for your model, as thermal management bugs are occasionally identified and fixed in these updates. Consider whether the device has recently been used in a notably warmer environment than usual, such as direct sunlight or an un-air-conditioned space, since ambient temperature meaningfully affects cooling performance.

Resolution
If overheating persists after closing unnecessary applications and confirming proper ventilation, the device should be sent for a physical inspection, since internal dust buildup or a failing fan cannot be resolved through software alone and continued use in this state risks permanent hardware damage. Devices showing signs of physical damage, unusual smells, or vibration should be taken out of service immediately rather than waiting for a scheduled inspection."""
},
{
    "kb_id": 'KB-106',
    "title": 'Installing and Licensing Software Requests',
    "category": 'Software',
    "tags": ['Software', 'License', 'Installation'],
    "last_updated": '2026-07-05',
    "priority": 'Medium',
    "version": '1.2',
    "author": 'Application Support Team',
    "content": """Overview
This article explains the process for requesting new software installations and resolving the most common license activation errors that follow. Because company devices are locked down for security reasons, most software cannot simply be installed directly by employees, and understanding the approval workflow helps set the right expectations for how long a request will take.

Symptoms
Software may fail to install due to permission restrictions, displaying a generic access denied message rather than clearly stating that administrator rights are required. Some applications show a license activation error immediately on first launch, even though the company holds a valid license for that tool. Others display a trial expired message despite the employee never having used a personal trial version, which usually indicates the license was not correctly applied rather than a genuine expiration.

Troubleshooting Steps
Confirm you have submitted a software request through the internal IT portal, as most applications require pre-approval before installation is technically possible on a managed company device, regardless of whether you have local admin rights. If installation fails specifically due to permissions, this almost always means administrator rights are required for that installer, which standard user accounts intentionally do not have by default as a security control. For license activation errors specifically, verify you are connected to the company network or VPN at the moment of activation, since many license servers only validate against devices reachable on the internal network and will fail silently otherwise. If the license error appears intermittently rather than consistently, this can indicate the license pool for that application is temporarily exhausted rather than a problem with your specific account.

Resolution
Standard software requests are typically fulfilled within one business day once formally approved through the portal, though complex or higher-cost software may take longer pending budget approval. License activation errors experienced while on VPN usually resolve within a few minutes of reconnecting and relaunching the application. Persistent errors after confirming network connectivity should be reported with the exact error code shown, as this significantly speeds up diagnosis compared to a general description of the problem."""
},
{
    "kb_id": 'KB-107',
    "title": 'Reporting Suspicious Emails and Phishing Attempts',
    "category": 'Security',
    "tags": ['Security', 'Phishing', 'Email'],
    "last_updated": '2026-07-12',
    "priority": 'Low',
    "version": '1.3',
    "author": 'Security Team',
    "content": """Overview
This guide explains how to identify and report phishing emails in order to protect your account and company data. Phishing remains one of the most common ways attackers gain initial access to corporate systems, and the speed at which a suspicious email is reported often determines how contained the resulting incident is. Every employee plays a role in this first line of defense, regardless of technical background.

Symptoms
Suspicious emails often contain urgent or threatening language demanding immediate action, such as claims that an account will be closed within hours unless credentials are confirmed. They frequently include requests for login credentials or payment information sent through email rather than a secure portal, unexpected attachments from senders you were not expecting to hear from, or sender addresses that closely mimic legitimate contacts with subtle misspellings that are easy to miss at a glance. Some phishing attempts are highly targeted and reference real internal projects or colleagues, making them harder to spot than generic scam emails.

Troubleshooting Steps
Never click links or download attachments from emails you were not expecting to receive, even if they appear to come from a known contact, since sender addresses can be spoofed or a genuine contact's account may itself be compromised. Hover over links without clicking to preview the actual destination URL shown at the bottom of most email clients, and compare it carefully against the domain you would expect. Check the sender's full email address rather than just the display name, since attackers frequently spoof a familiar display name while using a completely different underlying address. If you have already clicked a suspicious link or entered credentials, disconnect from the network immediately rather than continuing to investigate on your own, since time matters more than gathering additional details at that point.

Resolution
Use the Report Phishing button available in your email client to forward suspicious messages directly to the security team for analysis, which also removes the message from your inbox safely. If you entered credentials on a suspicious page, change your password immediately through a separate, trusted device and notify security right away, as your account may require additional monitoring or a forced credential rotation depending on what was exposed."""
},
{
    "kb_id": 'KB-108',
    "title": 'Wireless Network Connectivity Issues',
    "category": 'Networking',
    "tags": ['WiFi', 'Network', 'Connectivity'],
    "last_updated": '2026-06-25',
    "priority": 'High',
    "version": '1.0',
    "author": 'Network Team',
    "content": """Overview
This article covers troubleshooting steps for employees experiencing unstable or unavailable WiFi connections in the office. Office wireless networks serve dozens or hundreds of devices simultaneously, and connectivity issues can stem from the individual device, a specific access point, or the broader network infrastructure, so identifying which category applies is the first step toward a fast resolution.

Symptoms
Devices may fail to detect the office wireless network entirely despite it being visible to colleagues nearby, connect successfully but show a limited connectivity warning with no actual internet access, or experience frequent disconnections throughout the day at seemingly random intervals. Some employees notice the issue is worse in specific areas of the building, which is a useful clue for diagnosis.

Troubleshooting Steps
Toggle WiFi off and on from your device settings to force a fresh rescan for available networks, which resolves a surprising number of detection issues on its own. Forget the network entirely on your device and reconnect using fresh credentials, since saved network profiles can occasionally become corrupted after a password change or configuration update on the network side. Move closer to a known access point if you are in an area with historically weak coverage, such as stairwells, basements, or rooms with significant physical obstruction. Restart your device's network adapter through device manager if disconnections persist after reconnecting normally, as this clears a lower-level driver state that a simple toggle does not always reach.

Resolution
If multiple users in the same physical area report connectivity issues at the same time, this strongly indicates an access point failure rather than an individual device problem, and should be reported to network administration with the specific location and approximate time the issue began. Isolated single-device issues that persist after all steps above should be reported with the device model and operating system version, as certain hardware and driver combinations are more prone to specific wireless issues than others."""
},
{
    "kb_id": 'KB-109',
    "title": 'Multi-Factor Authentication Setup and Issues',
    "category": 'Security',
    "tags": ['Security', 'MFA', 'Authentication'],
    "last_updated": '2026-07-08',
    "priority": 'Medium',
    "version": '1.1',
    "author": 'Security Team',
    "content": """Overview
This guide covers setting up multi-factor authentication and resolving the most common issues when authentication codes fail to work as expected. MFA is a required security control across all company systems, and while it significantly reduces the risk of account compromise, a small number of predictable configuration issues account for the large majority of support requests related to it.

Symptoms
The authenticator app may fail to generate valid codes at all, codes may be rejected as expired immediately after being generated with no visible delay, or SMS-based codes may simply never arrive despite the phone number appearing correct in the account settings. Some users report the app working fine for weeks and then suddenly failing after an update to their phone's operating system.

Troubleshooting Steps
Confirm the time on your mobile device is set to automatic and synced correctly, as authenticator apps rely on precise time matching between your device and the authentication server, and even a small clock drift is enough to invalidate every generated code. If codes are consistently rejected despite correct time settings, remove and re-add the account within your authenticator app entirely, which regenerates the underlying secret key rather than attempting to reuse a potentially corrupted one. For SMS-based codes specifically, confirm your registered phone number is current and correctly formatted in the employee portal, since even a single incorrect digit will cause silent delivery failure with no error shown to the user.

Resolution
Time synchronization issues resolve immediately once automatic time is enabled and the device has had a moment to resync with the network time server. If you have lost access to your authenticator device entirely, whether through loss, theft, or a factory reset, contact IT security directly for identity verification and account recovery, as this specific scenario cannot be self-serviced for security reasons and requires manual verification of your identity through an alternate channel."""
},
{
    "kb_id": 'KB-110',
    "title": 'Printer Connectivity and Print Queue Issues',
    "category": 'Hardware',
    "tags": ['Hardware', 'Printer'],
    "last_updated": '2026-06-18',
    "priority": 'Low',
    "version": '1.2',
    "author": 'Hardware Support Team',
    "content": """Overview
This article addresses common printer issues including failure to print, stuck print queues, and connectivity problems affecting shared office printers. Because printers are typically shared across many employees, a single stuck job or configuration issue can quietly affect everyone in a department, making quick diagnosis particularly valuable.

Symptoms
Print jobs may appear stuck in the queue indefinitely with no visible progress or error, the printer may show as offline in the system despite clearly being powered on and connected to the network, or documents may print successfully but with formatting errors such as incorrect margins or missing images. Some users notice that only their own jobs are affected while colleagues print normally, which is a useful signal that the issue is local rather than printer-wide.

Troubleshooting Steps
Clear the print queue completely and resend the job rather than attempting to resume a stuck one, since stuck jobs frequently block all subsequent print requests from that device until manually cleared. Confirm the printer is on the same network as your device, particularly after any recent network changes or if you have switched between office locations, since printers are often configured for a specific subnet. Restart the print spooler service on your machine, which resolves the majority of queue-related freezes without requiring any changes to the printer itself. Update or reinstall the printer driver if formatting errors persist across multiple different documents, since a corrupted or outdated driver is the most common cause of this specific symptom.

Resolution
Most queue issues resolve after clearing stuck jobs and restarting the print spooler, which together resolve the large majority of reported cases without further escalation. If the printer remains offline after completing these steps, check the physical network cable or WiFi connection on the printer itself, as hardware-level disconnection on the printer's side is a common root cause that is easy to overlook when troubleshooting only from the computer."""
},
]

def get_articles():
    return articles