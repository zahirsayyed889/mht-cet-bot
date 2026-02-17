"""
╔════════════════════════════════════════════════════════════════════════╗
║          MHT-CET WARRIOR BOT - ULTIMATE EDITION                        ║
║                    🎓 DEVELOPED BY PROOFY GAMERZ 🎓                    ║
║                    youtube.com/@proofygamerz                           ║
║                                                                        ║
║  ✅ 735 Questions (49 Chapters)  ✅ Production Ready                  ║
║  ✅ Complete MHT-CET Coverage    ✅ Flask Server Included             ║
║                                                                        ║
║  Copyright © 2024-2025 Proofy Gamerz. All Rights Reserved.            ║
╚════════════════════════════════════════════════════════════════════════╝

🚀 COPY-PASTE READY - DEPLOY IMMEDIATELY!
For MHT-CET Aspirants - Helping Students Achieve Their Dreams!
"""

import telebot
from telebot import types
import json
import random
import time
import os
import glob
from datetime import datetime, timedelta
from collections import defaultdict
import threading

# =========================
# CONFIGURATION
# =========================

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7240890804:AAEwjjDk1gh1hFoJgmNZ9ExZUNKGq6TnI2I")
DATA_DIR = "bot_data"
USER_DATA_FILE = os.path.join(DATA_DIR, "users.json")

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# Create data directory
os.makedirs(DATA_DIR, exist_ok=True)

# =========================
# DATA STRUCTURES
# =========================

SUBJECTS = {
    "Physics": {
        "emoji": "📘",
        "chapters": [
            "Rotational Dynamics",
            "Mechanical Properties of Fluids",
            "Kinetic Theory of Gases and Radiation",
            "Thermodynamics",
            "Oscillations",
            "Superposition of Waves",
            "Wave Optics",
            "Electrostatics",
            "Current Electricity",
            "Magnetic Fields due to Electric Current",
            "Magnetic Materials",
            "Electromagnetic Induction",
            "AC Circuits",
            "Dual Nature of Radiation and Matter",
            "Structure of Atoms and Nuclei",
            "Semiconductor Devices"
        ]
    },
    "Chemistry": {
        "emoji": "🧪",
        "chapters": [
            "Solid State",
            "Solutions",
            "Ionic Equilibria",
            "Chemical Thermodynamics",
            "Electrochemistry",
            "Chemical Kinetics",
            "Elements of Groups 16, 17 and 18",
            "Transition and Inner Transition Elements",
            "Coordination Compounds",
            "Halogen Derivatives",
            "Alcohols, Phenols and Ethers",
            "Aldehydes, Ketones and Carboxylic Acids",
            "Amines",
            "Biomolecules",
            "Introduction to Polymer Chemistry",
            "Green Chemistry and Nanochemistry"
        ]
    },
    "Mathematics": {
        "emoji": "📐",
        "chapters": [
            "Mathematical Logic",
            "Matrices",
            "Trigonometric Functions",
            "Pair of Straight Lines",
            "Vectors",
            "Three Dimensional Geometry",
            "Line and Plane",
            "Linear Programming",
            "Continuity",
            "Differentiation",
            "Applications of Derivatives",
            "Integration",
            "Definite Integration",
            "Application of Definite Integration",
            "Differential Equations",
            "Probability Distribution",
            "Bernoulli Trials and Binomial Distribution"
        ]
    }
}

DIFFICULTY_LEVELS = {
    "🟢 Easy": {"level": "easy", "desc": "Concept Builders"},
    "🟡 Moderate": {"level": "moderate", "desc": "CET Level"},
    "🔴 Hard": {"level": "hard", "desc": "Rank Booster"}
}

# =========================
# LOAD ALL CHAPTER JSON FILES
# =========================

def load_all_chapters():
    """
    Automatically loads all chapter JSON files from the 'chapters/' folder.
    Each file has structure: { "subject": ..., "chapter": ..., "questions": { "easy": [...], "moderate": [...], "hard": [...] } }
    Returns a nested dict: questions[subject][chapter] = { "easy": [...], ... }
    """
    questions = {}
    chapters_dir = "chapters"

    if not os.path.exists(chapters_dir):
        print(f"⚠️  Warning: '{chapters_dir}/' folder not found! Using empty question bank.")
        return questions

    json_files = sorted(glob.glob(os.path.join(chapters_dir, "*.json")))

    if not json_files:
        print(f"⚠️  Warning: No JSON files found in '{chapters_dir}/'!")
        return questions

    loaded = 0
    errors = 0
    for filepath in json_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            subject = data.get("subject")
            chapter = data.get("chapter")
            chapter_questions = data.get("questions", {})

            if not subject or not chapter:
                print(f"⚠️  Skipping {filepath} - missing subject or chapter field")
                errors += 1
                continue

            if subject not in questions:
                questions[subject] = {}

            questions[subject][chapter] = chapter_questions
            loaded += 1

        except Exception as e:
            print(f"❌ Error loading {filepath}: {e}")
            errors += 1

    total_q = sum(
        len(q_list)
        for subj in questions.values()
        for chap in subj.values()
        for q_list in chap.values()
    )

    print(f"📚 Loaded {loaded} chapters ({total_q} total questions)" + (f" | {errors} errors" if errors else ""))
    return questions


# =========================
# PERSISTENT STORAGE SYSTEM
# =========================

class DataManager:
    """Thread-safe data persistence manager"""

    def __init__(self):
        self.lock = threading.Lock()
        self.users = self.load_users()
        self.questions = load_all_chapters()

    def load_users(self):
        """Load user data from file"""
        try:
            if os.path.exists(USER_DATA_FILE):
                with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}

    def save_users(self):
        """Save user data to file"""
        try:
            with self.lock:
                with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving users: {e}")

    def get_user(self, chat_id):
        """Get or create user profile"""
        chat_id = str(chat_id)
        if chat_id not in self.users:
            self.users[chat_id] = {
                "name": None,
                "created": datetime.now().isoformat(),
                "stats": {
                    "total_attempted": 0,
                    "total_correct": 0,
                    "subject_stats": {subject: {"attempted": 0, "correct": 0} for subject in SUBJECTS},
                    "chapter_stats": {},
                    "difficulty_stats": {level: {"attempted": 0, "correct": 0} for level in ["easy", "moderate", "hard"]},
                    "streak_days": 0,
                    "last_practice": None
                },
                "current_session": None,
                "question_history": []
            }
            self.save_users()
        return self.users[chat_id]

    def update_stats(self, chat_id, subject, chapter, difficulty, correct):
        """Update user statistics"""
        user = self.get_user(chat_id)
        stats = user["stats"]

        stats["total_attempted"] += 1
        if correct:
            stats["total_correct"] += 1

        if subject in stats["subject_stats"]:
            stats["subject_stats"][subject]["attempted"] += 1
            if correct:
                stats["subject_stats"][subject]["correct"] += 1

        chapter_key = f"{subject}_{chapter}"
        if chapter_key not in stats["chapter_stats"]:
            stats["chapter_stats"][chapter_key] = {"attempted": 0, "correct": 0}
        stats["chapter_stats"][chapter_key]["attempted"] += 1
        if correct:
            stats["chapter_stats"][chapter_key]["correct"] += 1

        if difficulty in stats["difficulty_stats"]:
            stats["difficulty_stats"][difficulty]["attempted"] += 1
            if correct:
                stats["difficulty_stats"][difficulty]["correct"] += 1

        last_practice = stats.get("last_practice")
        if last_practice:
            last_date = datetime.fromisoformat(last_practice).date()
            if (datetime.now().date() - last_date).days == 1:
                stats["streak_days"] += 1
            elif (datetime.now().date() - last_date).days > 1:
                stats["streak_days"] = 1
        else:
            stats["streak_days"] = 1

        stats["last_practice"] = datetime.now().isoformat()
        self.save_users()

    def start_session(self, chat_id, subject, chapter, difficulty):
        """Start a practice session"""
        user = self.get_user(chat_id)

        if subject in self.questions and chapter in self.questions[subject]:
            questions = self.questions[subject][chapter].get(difficulty, [])
            if questions:
                shuffled = questions.copy()
                random.shuffle(shuffled)

                user["current_session"] = {
                    "subject": subject,
                    "chapter": chapter,
                    "difficulty": difficulty,
                    "questions": shuffled,
                    "available": list(range(len(shuffled))),
                    "current_index": None,
                    "session_correct": 0,
                    "session_total": 0
                }
                self.save_users()
                return True
        return False

    def get_next_question(self, chat_id):
        """Get next random question from current session"""
        user = self.get_user(chat_id)
        session = user.get("current_session")

        if not session:
            return None

        if not session["available"]:
            session["available"] = list(range(len(session["questions"])))
            random.shuffle(session["available"])

        idx = random.choice(session["available"])
        session["available"].remove(idx)
        session["current_index"] = idx

        self.save_users()
        return session["questions"][idx]

    def check_answer(self, chat_id, answer):
        """Check if answer is correct and update stats"""
        user = self.get_user(chat_id)
        session = user.get("current_session")

        if not session or session["current_index"] is None:
            return None

        question = session["questions"][session["current_index"]]
        correct = (answer == question["ans"])

        session["session_total"] += 1
        if correct:
            session["session_correct"] += 1

        self.update_stats(
            chat_id,
            session["subject"],
            session["chapter"],
            session["difficulty"],
            correct
        )

        return {
            "correct": correct,
            "answer": question["ans"],
            "explanation": question["exp"]
        }

    def end_session(self, chat_id):
        """End current session"""
        user = self.get_user(chat_id)
        session = user.get("current_session")

        if session:
            result = {
                "total": session["session_total"],
                "correct": session["session_correct"],
                "accuracy": (session["session_correct"] / session["session_total"] * 100) if session["session_total"] > 0 else 0
            }
            user["current_session"] = None
            self.save_users()
            return result
        return None


# Initialize data manager
data_manager = DataManager()

# =========================
# USER SESSION STATE
# =========================

user_states = {}

def set_state(chat_id, state, data=None):
    user_states[chat_id] = {"state": state, "data": data or {}}

def get_state(chat_id):
    return user_states.get(chat_id, {}).get("state")

def get_state_data(chat_id):
    return user_states.get(chat_id, {}).get("data", {})

def clear_state(chat_id):
    if chat_id in user_states:
        del user_states[chat_id]

# =========================
# UI HELPER FUNCTIONS
# =========================

def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📘 Physics Practice"),
        types.KeyboardButton("🧪 Chemistry Practice"),
        types.KeyboardButton("📐 Mathematics Practice"),
        types.KeyboardButton("🎯 Mixed CET Test"),
        types.KeyboardButton("📊 My Performance"),
        types.KeyboardButton("ℹ️ About")
    )
    return markup

def create_back_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🔙 Back", "🏠 Main Menu")
    return markup

def create_chapter_menu(chapters):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for chapter in chapters:
        markup.add(types.KeyboardButton(chapter))
    markup.row("🔙 Back", "🏠 Main Menu")
    return markup

def create_difficulty_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for diff_text, diff_data in DIFFICULTY_LEVELS.items():
        markup.add(types.KeyboardButton(f"{diff_text} - {diff_data['desc']}"))
    markup.row("🔙 Back", "🏠 Main Menu")
    return markup

def create_practice_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("⏭️ Next Question", "❌ End Session")
    markup.row("🏠 Main Menu")
    return markup

def send_animated_message(chat_id, messages, final_text, final_markup=None):
    msg = bot.send_message(chat_id, messages[0])
    for text in messages[1:]:
        time.sleep(0.4)
        try:
            bot.edit_message_text(text, chat_id, msg.message_id)
        except:
            pass
    time.sleep(0.4)
    try:
        bot.edit_message_text(final_text, chat_id, msg.message_id,
                              reply_markup=final_markup, parse_mode="Markdown")
    except:
        bot.send_message(chat_id, final_text, reply_markup=final_markup, parse_mode="Markdown")

# =========================
# COMMAND HANDLERS
# =========================

@bot.message_handler(commands=['start'])
def start(message):
    try:
        data_manager.get_user(message.chat.id)
        send_animated_message(
            message.chat.id,
            [
                "⚡ Initializing MHT-CET Engine...",
                "🔬 Loading Question Banks...",
                "📚 Preparing Your Dashboard...",
                "🚀 Ready to Launch..."
            ],
            final_text=(
                "🎯 *WELCOME TO MHT-CET WARRIOR* 🎯\n\n"
                "Your Ultimate Competitive Exam Preparation Platform\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "✅ 49 Chapters Coverage\n"
                "✅ 735 Questions Ready\n"
                "✅ 3 Difficulty Levels\n"
                "✅ Infinite Practice Mode\n"
                "✅ Real-time Analytics\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                "💡 *TIP:* Practice daily to maintain your streak!\n\n"
                "⬇️ *First time?* Subscribe to support development ⬇️"
            ),
            final_markup=types.InlineKeyboardMarkup([
                [types.InlineKeyboardButton("🔔 Subscribe - Proofy Gamerz",
                                            url="https://youtube.com/@proofygamerz")],
                [types.InlineKeyboardButton("🚀 Start Practicing", callback_data="main_menu")]
            ])
        )
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Error starting bot. Please try /start again.")
        print(f"Start error: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def main_menu_callback(call):
    try:
        bot.answer_callback_query(call.id)
        user = data_manager.get_user(call.message.chat.id)
        stats = user["stats"]
        accuracy = (stats["total_correct"] / stats["total_attempted"] * 100) if stats["total_attempted"] > 0 else 0

        text = (
            f"🎯 *MHT-CET PRACTICE DASHBOARD*\n\n"
            f"📊 *Your Stats:*\n"
            f"   Questions: {stats['total_attempted']} | Correct: {stats['total_correct']}\n"
            f"   Accuracy: {accuracy:.1f}%\n"
            f"   Streak: {stats['streak_days']} days 🔥\n\n"
            f"Choose your practice mode:"
        )
        bot.send_message(call.message.chat.id, text,
                         reply_markup=create_main_menu(),
                         parse_mode="Markdown")
    except Exception as e:
        bot.send_message(call.message.chat.id, "Error loading menu. Please try /start")
        print(f"Menu error: {e}")

# =========================
# SUBJECT SELECTION
# =========================

@bot.message_handler(func=lambda m: m.text in ["📘 Physics Practice", "🧪 Chemistry Practice", "📐 Mathematics Practice"])
def select_subject(message):
    try:
        subject_map = {
            "📘 Physics Practice": "Physics",
            "🧪 Chemistry Practice": "Chemistry",
            "📐 Mathematics Practice": "Mathematics"
        }
        subject = subject_map[message.text]
        set_state(message.chat.id, "selecting_chapter", {"subject": subject})

        chapters = SUBJECTS[subject]["chapters"]
        emoji = SUBJECTS[subject]["emoji"]

        text = (
            f"{emoji} *{subject.upper()} PRACTICE*\n\n"
            f"📚 {len(chapters)} Chapters Available\n\n"
            f"Select a chapter to begin:"
        )
        bot.send_message(message.chat.id, text,
                         reply_markup=create_chapter_menu(chapters),
                         parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "Error loading chapters. Please try again.")
        print(f"Subject selection error: {e}")

# =========================
# CHAPTER SELECTION
# =========================

@bot.message_handler(func=lambda m: get_state(m.chat.id) == "selecting_chapter")
def select_chapter(message):
    try:
        if message.text in ["🔙 Back", "🏠 Main Menu"]:
            go_back(message) if message.text == "🔙 Back" else go_main_menu(message)
            return

        state_data = get_state_data(message.chat.id)
        subject = state_data.get("subject")
        chapter = message.text

        if chapter not in SUBJECTS[subject]["chapters"]:
            return

        set_state(message.chat.id, "selecting_difficulty", {"subject": subject, "chapter": chapter})

        text = (
            f"📖 *{chapter}*\n\n"
            f"Choose your difficulty level:\n\n"
            f"🟢 Easy - Build foundation concepts\n"
            f"🟡 Moderate - CET exam level questions\n"
            f"🔴 Hard - Rank booster challenges"
        )
        bot.send_message(message.chat.id, text,
                         reply_markup=create_difficulty_menu(),
                         parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "Error. Please select chapter again.")
        print(f"Chapter selection error: {e}")

# =========================
# DIFFICULTY SELECTION & START PRACTICE
# =========================

@bot.message_handler(func=lambda m: get_state(m.chat.id) == "selecting_difficulty")
def select_difficulty(message):
    try:
        if message.text in ["🔙 Back", "🏠 Main Menu"]:
            go_back(message) if message.text == "🔙 Back" else go_main_menu(message)
            return

        state_data = get_state_data(message.chat.id)
        subject = state_data.get("subject")
        chapter = state_data.get("chapter")

        difficulty = None
        for diff_text, diff_data in DIFFICULTY_LEVELS.items():
            if message.text.startswith(diff_text):
                difficulty = diff_data["level"]
                break

        if not difficulty:
            return

        send_animated_message(
            message.chat.id,
            [
                "🔄 Loading Questions...",
                "🎲 Shuffling Question Bank...",
                "⚡ Preparing Your Challenge..."
            ],
            final_text=""
        )

        success = data_manager.start_session(message.chat.id, subject, chapter, difficulty)

        if success:
            set_state(message.chat.id, "practicing")
            send_next_question(message.chat.id)
        else:
            bot.send_message(message.chat.id,
                             "❌ No questions available for this combination.\n"
                             "More questions coming soon!",
                             reply_markup=create_main_menu())
            clear_state(message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, "Error starting practice. Please try again.")
        print(f"Difficulty selection error: {e}")

# =========================
# PRACTICE SESSION
# =========================

def send_next_question(chat_id):
    try:
        question = data_manager.get_next_question(chat_id)
        if not question:
            bot.send_message(chat_id, "No more questions available!")
            return

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for option in question["opts"]:
            markup.add(types.KeyboardButton(option))
        markup.row("❌ End Session", "🏠 Main Menu")

        user = data_manager.get_user(chat_id)
        session = user["current_session"]

        diff_emoji = "🟢" if session['difficulty'] == 'easy' else "🟡" if session['difficulty'] == 'moderate' else "🔴"
        text = (
            f"🎯 *{session['subject']} - {session['chapter']}*\n"
            f"{diff_emoji} {session['difficulty'].title()} Level\n\n"
            f"❓ *Question {session['session_total'] + 1}*\n\n"
            f"{question['q']}\n\n"
            f"Select your answer:"
        )
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(chat_id, "Error loading question. Please try again.")
        print(f"Send question error: {e}")

@bot.message_handler(func=lambda m: get_state(m.chat.id) == "practicing")
def handle_answer(message):
    try:
        if message.text == "❌ End Session":
            end_practice_session(message.chat.id)
            bot.send_message(message.chat.id, "Returning to main menu...", reply_markup=create_main_menu())
            clear_state(message.chat.id)
            return
        elif message.text == "🏠 Main Menu":
            end_practice_session(message.chat.id)
            bot.send_message(message.chat.id, "Session ended.", reply_markup=create_main_menu())
            clear_state(message.chat.id)
            return

        result = data_manager.check_answer(message.chat.id, message.text)
        if not result:
            return

        if result["correct"]:
            text = (
                "✅ *CORRECT!* 🎉\n\n"
                f"💡 *Concept:*\n{result['explanation']}\n\n"
                "Press ⏭️ Next Question"
            )
        else:
            text = (
                "❌ *INCORRECT*\n\n"
                f"✔️ *Correct Answer:* {result['answer']}\n\n"
                f"💡 *Concept:*\n{result['explanation']}\n\n"
                "Press ⏭️ Next Question"
            )

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("⏭️ Next Question")
        markup.row("❌ End Session", "🏠 Main Menu")

        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")
        set_state(message.chat.id, "waiting_next")

    except Exception as e:
        bot.send_message(message.chat.id, "Error processing answer. Please try again.")
        print(f"Answer handling error: {e}")

@bot.message_handler(func=lambda m: get_state(m.chat.id) == "waiting_next" and m.text == "⏭️ Next Question")
def next_question_handler(message):
    set_state(message.chat.id, "practicing")
    send_next_question(message.chat.id)

def end_practice_session(chat_id):
    try:
        result = data_manager.end_session(chat_id)
        if result:
            accuracy = result["accuracy"]
            if accuracy >= 80:
                perf = "🏆 EXCELLENT!"
            elif accuracy >= 60:
                perf = "👏 GOOD WORK!"
            elif accuracy >= 40:
                perf = "📚 KEEP PRACTICING!"
            else:
                perf = "💪 DON'T GIVE UP!"

            text = (
                f"{perf}\n\n"
                f"📊 *SESSION SUMMARY*\n\n"
                f"Total Questions: {result['total']}\n"
                f"Correct Answers: {result['correct']}\n"
                f"Accuracy: {accuracy:.1f}%\n\n"
                f"{'⭐' * min(5, int(accuracy/20))}\n\n"
                f"Keep practicing to improve! 🚀"
            )
            bot.send_message(chat_id, text, parse_mode="Markdown")
        clear_state(chat_id)
    except Exception as e:
        print(f"End session error: {e}")

# =========================
# PERFORMANCE DASHBOARD
# =========================

@bot.message_handler(func=lambda m: m.text == "📊 My Performance")
def show_performance(message):
    try:
        user = data_manager.get_user(message.chat.id)
        stats = user["stats"]

        total = stats["total_attempted"]
        correct = stats["total_correct"]
        accuracy = (correct / total * 100) if total > 0 else 0

        subject_text = ""
        for subject, subj_stats in stats["subject_stats"].items():
            s_total = subj_stats["attempted"]
            s_correct = subj_stats["correct"]
            s_acc = (s_correct / s_total * 100) if s_total > 0 else 0
            emoji = SUBJECTS[subject]["emoji"]
            subject_text += f"{emoji} {subject}: {s_acc:.0f}% ({s_correct}/{s_total})\n"

        diff_text = ""
        for level, level_stats in stats["difficulty_stats"].items():
            l_total = level_stats["attempted"]
            l_correct = level_stats["correct"]
            l_acc = (l_correct / l_total * 100) if l_total > 0 else 0
            icon = "🟢" if level == "easy" else "🟡" if level == "moderate" else "🔴"
            diff_text += f"{icon} {level.title()}: {l_acc:.0f}% ({l_correct}/{l_total})\n"

        streak_emoji = "🔥" if stats["streak_days"] > 0 else "💤"

        text = (
            f"📊 *YOUR PERFORMANCE DASHBOARD*\n\n"
            f"{'━' * 25}\n"
            f"*OVERALL STATS*\n"
            f"Questions Attempted: {total}\n"
            f"Correct Answers: {correct}\n"
            f"Overall Accuracy: {accuracy:.1f}%\n"
            f"Current Streak: {stats['streak_days']} days {streak_emoji}\n\n"
            f"{'━' * 25}\n"
            f"*SUBJECT WISE*\n{subject_text}\n"
            f"{'━' * 25}\n"
            f"*DIFFICULTY WISE*\n{diff_text}\n"
            f"{'━' * 25}\n\n"
            f"💡 *Keep practicing daily to improve!*"
        )

        bot.send_message(message.chat.id, text,
                         reply_markup=create_back_menu(),
                         parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "Error loading performance data.")
        print(f"Performance error: {e}")

# =========================
# MIXED CET TEST
# =========================

@bot.message_handler(func=lambda m: m.text == "🎯 Mixed CET Test")
def mixed_test(message):
    bot.send_message(
        message.chat.id,
        "🎯 *MIXED CET TEST*\n\n"
        "🚧 *Coming Soon!*\n\n"
        "This feature will simulate a real MHT-CET exam with:\n"
        "✅ 20 random questions from all subjects\n"
        "✅ Time-based progression\n"
        "✅ Detailed scorecard\n\n"
        "Stay tuned! 🚀",
        reply_markup=create_back_menu(),
        parse_mode="Markdown"
    )

# =========================
# ABOUT & INFO
# =========================

@bot.message_handler(func=lambda m: m.text == "ℹ️ About")
def about(message):
    text = (
        "ℹ️ *ABOUT MHT-CET WARRIOR BOT*\n\n"
        "🎯 *Mission:*\n"
        "Help MHT-CET aspirants ace their exams through unlimited practice "
        "and intelligent performance tracking.\n\n"
        "📚 *Coverage:*\n"
        "• 16 Physics Chapters\n"
        "• 16 Chemistry Chapters\n"
        "• 17 Mathematics Chapters\n"
        "• 735 Questions Total\n"
        "• 3 Difficulty Levels\n"
        "• Infinite Practice Mode\n\n"
        "✨ *Features:*\n"
        "• Real-time concept explanations\n"
        "• Advanced analytics dashboard\n"
        "• Persistent progress tracking\n"
        "• Daily streak monitoring\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "*Developed by: Proofy Gamerz*\n"
        "For MHT-CET Aspirants\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔔 Subscribe: youtube.com/@proofygamerz\n\n"
        "Good luck with your preparation! 🚀"
    )
    bot.send_message(message.chat.id, text,
                     reply_markup=create_back_menu(),
                     parse_mode="Markdown")

# =========================
# NAVIGATION HANDLERS
# =========================

@bot.message_handler(func=lambda m: m.text == "🔙 Back")
def go_back(message):
    state = get_state(message.chat.id)
    if state == "selecting_chapter":
        clear_state(message.chat.id)
        bot.send_message(message.chat.id, "Back to main menu", reply_markup=create_main_menu())
    elif state == "selecting_difficulty":
        state_data = get_state_data(message.chat.id)
        subject = state_data.get("subject")
        set_state(message.chat.id, "selecting_chapter", {"subject": subject})
        chapters = SUBJECTS[subject]["chapters"]
        bot.send_message(message.chat.id, "Select chapter:",
                         reply_markup=create_chapter_menu(chapters))
    else:
        clear_state(message.chat.id)
        bot.send_message(message.chat.id, "Main Menu", reply_markup=create_main_menu())

@bot.message_handler(func=lambda m: m.text == "🏠 Main Menu")
def go_main_menu(message):
    clear_state(message.chat.id)
    data_manager.end_session(message.chat.id)

    user = data_manager.get_user(message.chat.id)
    stats = user["stats"]
    accuracy = (stats["total_correct"] / stats["total_attempted"] * 100) if stats["total_attempted"] > 0 else 0

    text = (
        f"🏠 *MAIN MENU*\n\n"
        f"Quick Stats: {stats['total_attempted']} Q | {accuracy:.1f}% Accuracy\n"
        f"Streak: {stats['streak_days']} days 🔥"
    )
    bot.send_message(message.chat.id, text,
                     reply_markup=create_main_menu(),
                     parse_mode="Markdown")

# =========================
# CATCH-ALL HANDLER
# =========================

@bot.message_handler(func=lambda m: True)
def catch_all(message):
    bot.send_message(
        message.chat.id,
        "❓ I didn't understand that.\n\n"
        "Please use the menu buttons to navigate.",
        reply_markup=create_main_menu()
    )

# =========================
# START BOT
# =========================

if __name__ == "__main__":
    print("=" * 55)
    print("🚀 MHT-CET WARRIOR BOT - ULTIMATE EDITION")
    print("   Developed by: Proofy Gamerz")
    print("   YouTube: youtube.com/@proofygamerz")
    print("=" * 55)

    # ─── FIX: Remove any existing webhook / duplicate polling ───
    # This kills any lingering webhook and stops the 409 Conflict error.
    try:
        bot.remove_webhook()
        print("✅ Webhook cleared")
    except Exception as e:
        print(f"⚠️  Could not clear webhook: {e}")

    print("✅ Bot is running...")
    print("📊 Data persistence: ENABLED")
    print(f"📚 Question bank: {sum(len(c) for c in data_manager.questions.values())} chapters loaded")
    print("🔄 Infinite practice: ENABLED")
    print("📈 Analytics: ENABLED")
    print("=" * 55)

    # Flask Web Server for Render.com keep-alive
    from flask import Flask
    flask_app = Flask(__name__)

    @flask_app.route('/')
    def home():
        return """<html><head><title>MHT-CET Bot</title></head>
        <body style='font-family:Arial;text-align:center;padding:50px;
        background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;'>
        <h1>✅ MHT-CET WARRIOR BOT IS RUNNING!</h1>
        <h2>🎓 Developed by Proofy Gamerz</h2>
        <p>📺 YouTube: youtube.com/@proofygamerz</p>
        <hr><p><strong>Status: ACTIVE ✅</strong></p>
        <p>735 Questions | 49 Chapters | Version: 4.0</p></body></html>"""

    @flask_app.route('/health')
    def health():
        return {"status": "healthy", "bot": "running", "chapters": sum(len(c) for c in data_manager.questions.values())}

    def run_flask():
        port = int(os.environ.get('PORT', 10000))
        flask_app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print(f"🌐 Web server: Port {os.environ.get('PORT', 10000)} ✓")

    # ─── Start polling (single instance, no conflicts) ───
    print("🔄 Starting polling...")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60, restart_on_change=False)
        except Exception as e:
            print(f"❌ Polling error: {e}")
            print("🔄 Restarting in 5 seconds...")
            time.sleep(5)
