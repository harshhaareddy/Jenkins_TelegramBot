import configparser
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, ConversationHandler, CallbackQueryHandler, CommandHandler, CallbackContext
import jenkins
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Stages
DISPLAYJOBS, SET_ENV, SET_JIRA, PARAMETERS, TRIGGER_BUILD, CURRENT_BUILD_CANCEL_OPTION, CANCEL_BUILD = range(7)
# # Callback data
ONE, TWO, THREE, FOUR, FIVE, SIX = range(6)


def start(update: Update, context: CallbackContext):
    user = update.message.chat.username
    name = update.message.chat.first_name
    registeredUser = config.get('key', 'user')
    print(user)
    print(f'registeredUser===>>{registeredUser}')
    if user in registeredUser:
        text = """
                    𝐇𝐞𝐥𝐥𝐨, 𝐈 𝐚𝐦 𝐇𝐚𝐫𝐬𝐡𝐡𝐚𝐚'𝐬 𝐁𝐮𝐢𝐥𝐝𝐬 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐨𝐧 𝐁𝐎𝐓,
                    𝐈𝐧 𝐜𝐚𝐬𝐞 𝐨𝐟 𝐚𝐧𝐲 𝐩𝐫𝐨𝐛𝐥𝐞𝐦, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐧𝐝 𝐞𝐦𝐚𝐢𝐥 𝐭𝐨 email.harshhaa03@gmail.com\n
                    \n *****𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐭𝐡𝐞 𝐛𝐞𝐥𝐨𝐰 𝐎𝐩𝐭𝐢𝐨𝐧𝐬*****\n
                    """

        keyboard = [
            [
                InlineKeyboardButton("Show me the Jobs", callback_data=str(ONE)),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        update.message.reply_text(text, reply_markup=reply_markup)
        # Tell ConversationHandler that we're in state `FIRST` now
        return DISPLAYJOBS
    else:
        update.message.reply_text(f"𝐇𝐢 {name},\n 𝐲𝐨𝐮 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐚𝐜𝐜𝐞𝐬𝐬 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐧𝐧𝐞𝐥 ")


def one(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    global con
    con = jenkins.Jenkins(url='${{secrets.JENKINS_URL}}', username='${{secrets.JENKINS_UNAME}}', password='${{secrets.JENKINS_PASS}}')
    # print(con.get_jobs())
    l1 = con.get_jobs()
    l2 = []
    for i in l1:
        l2.append(i['name'])
    key = []
    for i in l2:
        key.append([InlineKeyboardButton(i, callback_data=i)])
    print(key)
    keyboard = key
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text='𝐁𝐞𝐥𝐨𝐰 𝐚𝐫𝐞 𝐭𝐡𝐞 𝐉𝐨𝐛𝐬', reply_markup=reply_markup)
    return SET_ENV


def two(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    query = update.callback_query
    global JobName
    JobName = query.data
    print(f'𝐉𝐨𝐛 𝐍𝐚𝐦𝐞 𝐢𝐬 {JobName}')
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("SIT", callback_data="SIT"),
            InlineKeyboardButton("PT", callback_data="PROD"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="𝐋𝐞𝐭𝐬 𝐅𝐢𝐫𝐬𝐭 𝐂𝐡𝐨𝐨𝐬𝐞 𝐭𝐡𝐞 𝐄𝐧𝐯𝐢𝐫𝐨𝐧𝐦𝐞𝐧𝐭 𝐅𝐢𝐫𝐬𝐭", reply_markup=reply_markup
    )
    return SET_JIRA


def three(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    query = update.callback_query
    global Env
    Env = query.data
    print(f'𝐓𝐡𝐞 𝐄𝐧𝐯 𝐢𝐬 {Env}')
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("YES", callback_data="Yes"),
            InlineKeyboardButton("NO", callback_data="No"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="𝐁𝐮𝐠 𝐋𝐨𝐠𝐠𝐢𝐧𝐠 𝐢𝐧 𝐉𝐢𝐫𝐚", reply_markup=reply_markup)
    return PARAMETERS


def four(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    query = update.callback_query
    global JIRA_stats
    JIRA_stats = query.data
    text = (f'******𝐁𝐞𝐥𝐨𝐰 𝐚𝐫𝐞 𝐭𝐡𝐞 𝐜𝐨𝐧𝐟𝐢𝐠𝐮𝐫𝐚𝐭𝐢𝐨𝐧 𝐭𝐡𝐚𝐭 𝐲𝐨𝐮 𝐡𝐚𝐯𝐞 𝐬𝐞𝐥𝐞𝐜𝐭𝐞𝐝 :******\n'
            f'\n𝐄𝐧𝐯 ={Env} \n 𝐉𝐈𝐑𝐀_𝐓𝐈𝐂𝐊𝐄𝐓 = {JIRA_stats} \n 𝐉𝐎𝐁 𝐍𝐀𝐌𝐄 = {JobName}\n'
            f'\n 𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐥𝐞𝐜𝐭 𝐟𝐫𝐨𝐦 𝐛𝐞𝐥𝐨𝐰 𝐨𝐩𝐭𝐢𝐨𝐧𝐬')
    global payload
    payload = {
        "ENV": Env,
        "Bug Logging in Jira": JIRA_stats
    }
    print(payload)
    keyboard = [
        [
            InlineKeyboardButton("Trigger build", callback_data="Trigger build"),
            InlineKeyboardButton("Cancel", callback_data="Cancel"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=text, reply_markup=reply_markup)
    return TRIGGER_BUILD


def trigger_jenkins_build(payload, jobName):
    try:
        print("+++++++++++++++++++++++++++++++++++++\n")
        print(jobName)
        print(payload)
        print("++++++++++++++++++++++++++++++++++++++\n")
        status = con.build_job(name=jobName, parameters=payload)
        print(status)
        print(f'{jobName} 𝐢𝐬 𝐭𝐫𝐢𝐠𝐠𝐞𝐫𝐞𝐝 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲')
        return True
    except Exception as e:
        print(f'{jobName} 𝐢𝐬 𝐧𝐨𝐭 𝐭𝐫𝐢𝐠𝐠𝐞𝐫𝐞𝐝 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲')
        print(e)
        return False


def five(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    query = update.callback_query
    print(query.data)
    if query.data == 'Trigger build':
        is_triggered = trigger_jenkins_build(payload=payload, jobName=JobName)
        print(f'is_triggered--->{is_triggered}')
        if is_triggered:
            bot = context.bot
            bot.send_message(chat_id=query.message.chat_id, message_id=query.message.message_id,
                             text="𝐁𝐮𝐢𝐥𝐝 𝐢𝐬 𝐭𝐫𝐢𝐠𝐠𝐞𝐫𝐞𝐝 ")
            # update.message.reply_text("Build triggered successfully", reply_markup=reply_markup)
            keyboard = [
                [
                    InlineKeyboardButton("Cancel Build", callback_data="Cancel Build"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id=query.message.chat_id, text="𝐈𝐧𝐜𝐚𝐬𝐞 𝐭𝐡𝐢𝐬 𝐁𝐮𝐢𝐥𝐝 𝐢𝐬 𝐭𝐫𝐢𝐠𝐠𝐞𝐫𝐞𝐝 𝐢𝐧𝐜𝐨𝐫𝐫𝐞𝐜𝐭𝐥𝐲 ",
                             reply_markup=reply_markup)
            return CURRENT_BUILD_CANCEL_OPTION
        else:
            print("Exception Occured")
            query.edit_message_text(text="𝐄𝐱𝐜𝐞𝐩𝐭𝐢𝐨𝐧 𝐎𝐜𝐜𝐮𝐫𝐞𝐝")
            return ConversationHandler.END
    elif query.data == 'Cancel':
        print('This needs to be cancelled')
        query.edit_message_text(text="𝐏𝐥𝐞𝐚𝐬𝐞 𝐛𝐞𝐠𝐢𝐧 𝐭𝐡𝐞 𝐜𝐡𝐚𝐭 𝐚𝐠𝐚𝐢𝐧 𝐰𝐢𝐭𝐡 𝐇𝐚𝐫𝐬𝐡𝐡𝐚𝐚 𝐁𝐮𝐢𝐥𝐝𝐬 𝐉𝐞𝐧𝐤𝐢𝐧𝐬 𝐁𝐎𝐓 𝐚𝐧𝐝 𝐭𝐡𝐢𝐬 𝐭𝐢𝐦𝐞 𝐜𝐡𝐨𝐨𝐬𝐞 𝐜𝐚𝐫𝐞𝐟𝐮𝐥𝐥𝐲")
        return ConversationHandler.END
    else:
        print("Incorrect")


def six(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    print(query.data)
    keyboard = [
        [
            InlineKeyboardButton("Cancel build", callback_data="Trigger build"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="𝐈𝐧𝐜𝐚𝐬𝐞 𝐭𝐡𝐢𝐬 𝐁𝐮𝐢𝐥𝐝 𝐢𝐬 𝐭𝐫𝐢𝐠𝐠𝐞𝐫𝐞𝐝 𝐢𝐧𝐜𝐨𝐫𝐫𝐞𝐜𝐭𝐥𝐲 ", reply_markup=reply_markup)
    return CANCEL_BUILD


def return_current_build():
    currentbuildExecution = con.get_running_builds()
    for i in currentbuildExecution:
        i.get('number')
        return i.get('number')


def seven(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    buildnumber = return_current_build()
    bot = context.bot
    try:
        stopbuild = con.stop_build(name=JobName, number=buildnumber)
        bot.send_message(chat_id=query.message.chat_id,
                         text=f"𝐁𝐮𝐢𝐥𝐝 {buildnumber} 𝐨𝐟 {JobName} 𝐉𝐨𝐛 𝐒𝐮𝐜𝐜𝐞𝐬𝐟𝐮𝐥𝐥𝐲 𝐬𝐭𝐨𝐩𝐩𝐞𝐝")
        return CANCEL_BUILD
    except Exception as E:
        print(E)
    return CANCEL_BUILD


def main():
    config.read('config.cfg')
    token = config.get('key', 'token')

    updater = Updater(token, use_context=True)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            DISPLAYJOBS: [CallbackQueryHandler(one)],
            SET_ENV: [CallbackQueryHandler(two)],
            SET_JIRA: [CallbackQueryHandler(three)],
            PARAMETERS: [CallbackQueryHandler(four)],
            TRIGGER_BUILD: [CallbackQueryHandler(five)],
            CURRENT_BUILD_CANCEL_OPTION: [CallbackQueryHandler(six)],
            CANCEL_BUILD: [CallbackQueryHandler(seven)]

        },
        fallbacks=[CommandHandler('start', start)],
    )
    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    main()
