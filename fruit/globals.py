import click

FRUITCONFIG_NAME = "fruitconfig.py"

FMT_STEPHEADER      = "🥝 Step {number}: {name}\n" + "-"* (click.get_terminal_size()[0] - 5)
FMT_TARGETHEADER    = "🍉 Making '{target}' ..."
FMT_SUBTARGETHEADER = "🍎 Making sub-target '{target}' ..." + ">"* (click.get_terminal_size()[0] - 5)

SHELLCHAR = '$ '

ICON_SUCC = "✅"
ICON_FAIL    = "❌"
ICON_SKIP    = "⏭"
ICON_BANANA  = "🍌" 

FMT_SKIPMESSAGE     = ICON_SKIP + "  The step was skipped. {reason}"
FMT_FAILMESSAGE     = ICON_BANANA + "  The step failed! {reason}"