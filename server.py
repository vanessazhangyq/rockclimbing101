from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, redirect, url_for, flash
import re
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


lessons = {
    "1": {
        "lesson_id": "1",
        "title": "How to safety fall in bouldering",
        "media": "http://valcursus.nl/media/posts/8/responsive/poster-md.png",
        "media_type": "vertical",
        "text":
            "The Tuck & Roll technique implies that you TUCK your arms as you jump down and ROLL backward to break the fall. Tucking your arms prevents you from landing on and potentially breaking your arms and rolling over takes pressure away from your knees.",
        "previous_lesson": "home",
        "next_lesson": "2"
    },
    "2": {
        "lesson_id": "2",
        "title": "Video Demo",
        "video": "https://www.youtube.com/embed/uOILi_HMi70?si=VW2cDSu85kFzBczp",
        "text": "",
        "previous_lesson": "1",
        "next_lesson": "3"
    },
    "3": {
        "lesson_id": "3",
        "title": "Step 1: T-rex",
        "media": "https://ih1.redbubble.net/image.852291934.8842/flat,750x,075,f-pad,750x1000,f8f8f8.u3.jpg",
        "media_type": "vertical",
        "text": "Just like a T-rex dinosaur - Land on your feet with bent knees & tuck your arms inside.",
        "previous_lesson": "2",
        "next_lesson": "4"
    },
    "4": {
        "lesson_id": "4",
        "title": "Step 2: Turtle",
        "media": "https://png.pngtree.com/png-clipart/20230813/original/pngtree-funny-tortoise-turtle-walking-climbing-rock-exotic-reptile-cartoon-picture-image_7909655.png",
        "media_type": "horizontal",
        "text": "Just like a turtle - Put chin on chest to avoid head injuries.",
        "previous_lesson": "3",
        "next_lesson": "5" 
    },
    "5": {
        "lesson_id": "5",
        "title": "Step 3: Roll",
        "media": "https://lh5.googleusercontent.com/proxy/MMyexNOu5E33wBjlzTkYGN9gDO29L6C8_No7PbdWkyVjzCMza4Aw51GsamHnQsDLM0FueiA5g-5HPWBfl1qUg72vBA",
        "media_type": "vertical",
        "text": "Roll back - Don't lean forward otherwise your face will hit the wall.",
        "previous_lesson": "4",
        "next_lesson": "6" 
    },
    "6": {
        "lesson_id": "6",
        "title": "Quick Check on Safety 1/2",
        "question": "Is the following statement True or False: You should roll forwards after landing with two feet.",
        "options": ["True", "False"],  
        "correct_answer": "False", 
        "previous_lesson": "5",
        "next_lesson": "7" 
    }, 
    "7": {
        "lesson_id": "7",
        "title": "Quick Check on Safety 2/2",
        "steps": ["T-rex", "Roll", "Turtle"],
        "previous_lesson": "6",
        "next_lesson": "8" 
    },
    "8": {
    "lesson_id": "8",
    "title": "Congratulations!",
    "media": "https://em-content.zobj.net/source/skype/289/party-popper_1f389.png", 
    "media_type": "square",
    "text": "You've completed the Safety section! Please click next to learn about the different climbing types!",
    "previous_lesson": "7",
    "next_lesson": "climbing_types/1"
    }
}

climbing_types_lessons = {
    "1": {
        "lesson_id": "1",
        "title": "Introduction to Climbing Types",
        "media": "https://media1.thehungryjpeg.com/thumbs2/ori_3749506_dvp8tk78yl6s4dzmurit1ssxf30xip51b173qqm9_young-climber-man-vector-rock-climbing-sport-different-poses-tourist-hiking-trekking-cartoon-character-illustration.jpg",
        "media_type": "horizontal",
        "text": "Discover different climbing types.",
        "previous_lesson": "8",
        "next_lesson": "2"
    },
    "2": {
        "lesson_id": "2",
        "title": "Bouldering",
        "media": "/static/images/bouldering.png",
        "media_type": "horizontal",
        "text": "The most common climbing in gym. No harness required.",
        "previous_lesson": "1", 
        "next_lesson": "3" 
    },
    "3": {
        "lesson_id": "3",
        "title": "Auto-belay",
        "media": "/static/images/auto-belay.png", 
        "media_type": "horizontal",
        "text": "There is a auto-belay machine at the top of the wall. Harness required. Don’t need belay partner.",
        "previous_lesson": "2", 
        "next_lesson": "4" 
    },
    "4": {
        "lesson_id": "4",
        "title": "Top rope belay",
        "media": "https://www.vdiffclimbing.com/wp-content/images/basics/basic-top-rope-belay/take-in-top-rope-belay-2.png", 
        "media_type": "horizontal",
        "text": "There is an anchor at the top. Harness required. Need a belay partner. ",
        "previous_lesson": "3", 
        "next_lesson": "5" 
    },
    "5": {
        "lesson_id": "5",
        "title": "Lead",
        "media": "https://scl.cornell.edu/sites/scl/files/2020-05/COE%20ROCK%20Lead5%20HRZ.jpg", 
        "media_type": "horizontal",
        "text": "Climber has to clip-in the rope as they go. Harness required. Need a belay partner.", 
        "previous_lesson": "4", 
        "next_lesson": "6" 
    },
    "6": {
        "lesson_id": "6",
        "title": "Quick Check on Climbing Types 1/1",
        "media": "https://www.vdiffclimbing.com/wp-content/images/sport/better-belayer/better-belayer-2.png",
        "media_type": "vertical",
        "text": "",
        "question": "Identify the type of climbing shown in the picture.",
        "options": ["Auto Belay", "Lead", "Top Rope Belay"],
        "correct_answer": "Lead",
        "previous_lesson": "5",
        "next_lesson": "7"
    },
    "7": {
    "lesson_id": "7",
    "title": "Congratulations!",
    "media": "https://em-content.zobj.net/source/skype/289/party-popper_1f389.png", 
    "media_type": "square",
    "text": "You've completed the Climbing Types section! Please click next to learn about the grading system!",
    "previous_lesson": "6",
    "next_lesson": "grading_systems/1"
    }
}

grading_systems_lessons = {
        "1": {
            "lesson_id": "1",
            "title": "Introduction to Grading Systems",
            "media": "https://i.pinimg.com/originals/a1/90/89/a1908956ebfbb4b3af9dd74d31f32109.jpg",
            "media_type": "horizontal",
            "text": "Discover the grading system!",
            "previous_lesson": "7",
            "next_lesson": "2"
        },
        "2": {
            "lesson_id": "2",
            "title": "V-Scale",
            "media": "https://i.pinimg.com/736x/5a/82/c1/5a82c17a8be23ffa049327140550ce77.jpg",
            "media_type": "vertical",
            "text": "V-Scale is the grading system for bouldering in America. As a beginner, start from V0 in gym.",
            "previous_lesson": "1", 
            "next_lesson": "3" 
        },
        "3": {
            "lesson_id": "3",
            "title": "Yosemite Decimal System (YDS)",
            "media": "https://miro.medium.com/v2/resize:fit:568/1*bF7mHd1xbTnoAoklPK37sw.png",
            "media_type": "grading",
            "text": "American Grading system for route climbing. In gym, you would typically find routes in 5.6 - 5.13 levels. As a beginner, start from 5.6",
            "previous_lesson": "2", 
            "next_lesson": "4",
        },
        "4": {
            "lesson_id": "4",
            "title": "Quick Check on Grading System 1/1",
            "media": "",
            "text": "",
            "question": "Is the following statement True or False: As a beginner, you will start at level 6.5 in the Yosemite Decimal System (YDS).",
            "options": ["True", "False"],  
            "correct_answer": "False",
            "previous_lesson": "3",
            "next_lesson": "5"
        },
        "5": {
            "lesson_id": "5",
            "title": "Congratulations!",
            "media": "https://em-content.zobj.net/source/skype/289/party-popper_1f389.png", 
            "media_type": "square",
            "text": "You've completed the Grading Systems section! Click 'Next' to continue your journey and become a rock climbing newbie!",
            "previous_lesson": "4",
            "next_lesson": "quiz/0"
        }
}

quiz_data = {
    "0": {"quiz_num": "0",  #start
          "title": "Test your knowledge now! 5 quiz questions in total.", 
          "media": "/static/images/quiz.png",
          "options": [], 
          "correct_answer": "", 
          "back": "/", 
          "next": "1"},
    "1": {"quiz_num": "1", 
          "title": "1. What’s wrong with this falling?", 
          "media": "https://youtu.be/vD4jf_iw5Dk?si=kkvJinFtn7Rm3xUH", 
          "options": ["Fall while spinning can hurt your ankles", "Falling sideways is safe"], 
          "correct_answer": "Fall while spinning can hurt your ankles", 
          "back": "0", 
          "next": "2"},
    "2": {"quiz_num": "2", 
          "title": "2. What’s the correct way for falling", 
          "options": ["T-rex, Turtle, Roll", "Roll, T-rex, Turtle"], 
          "correct_answer": "T-rex, Turtle, Roll", 
          "back": "1", 
          "next": "3"},
    "3": {"quiz_num": "3", 
          "title": "3. You should roll _____ after landing with two feet.", 
          "options": ["forwards", "backwards"], 
          "correct_answer": "backwards", 
          "back": "2", 
          "next": "4"},
    "4": {"quiz_num": "4", 
          "title": "4. What’s the type of climbing on the image?", 
          "media": "/static/images/bouldering.png", 
          "options": ["Auto-belay", "Lead", "Bouldering", "Top Rope"], 
          "correct_answer": "Bouldering", 
          "back": "3", 
          "next": "5"},
    "5": {"quiz_num": "5", 
          "title": "5. What is the grading system for bouldering?", 
          "options": ["YDS", "V-Scale"], 
          "correct_answer": "V-Scale", 
          "back": "4", 
          "next": "6"},
    "6": { #finish
        "quiz_num": "6", 
          "title": "Congratulation!", 
          "media": "/static/images/congratulation.png",
          "score": 0,
          "back": "5", 
          "next": "Result"}
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/safety')
def safety_index():
    return redirect(url_for('safety', lesson_id="1"))

@app.route('/safety/<lesson_id>')
def safety(lesson_id):
    lesson = lessons.get(lesson_id, None)
    if lesson is None:
        return redirect(url_for('home'))

    previous_lesson = lesson.get('previous_lesson')
    previous_lesson_url = url_for('home') if previous_lesson == "home" else url_for('safety', lesson_id=previous_lesson)

    next_lesson = lesson.get('next_lesson')
    if next_lesson.isdigit():
        next_lesson_url = url_for('safety', lesson_id=next_lesson)
    elif "climbing_types" in next_lesson:
        next_lesson_url = url_for('climbing_types', lesson_id=next_lesson.split('/')[-1])
    elif "grading_systems" in next_lesson:
        next_lesson_url = url_for('grading_systems', lesson_id=next_lesson.split('/')[-1])
    else:
        next_lesson_url = url_for('home')

    return render_template('safety.html', lesson=lesson, previous_lesson_url=previous_lesson_url, next_lesson_url=next_lesson_url)



@app.route('/safety/<lesson_id>/submit_quiz', methods=['POST'])
def submit_quiz(lesson_id):
    selected_option = request.form['quizAnswer']
    lesson = lessons.get(lesson_id, {})
    
    # Check if the selected answer is correct
    is_correct = selected_option == lesson.get('correct_answer')
    
    if is_correct:
        flash('Correct answer!', 'success')
    else:
        flash('Incorrect answer. Try again.', 'danger')
    
    return redirect(url_for('safety', lesson_id=lesson_id))

@app.route('/safety/submit_drag_and_drop_quiz', methods=['POST'])
def submit_drag_and_drop_quiz():
    step1_answer = request.form.get('step1')
    step2_answer = request.form.get('step2')
    step3_answer = request.form.get('step3')

    lesson_id = '7'  # ID for the drag-and-drop quiz lesson

    # Check if the answers are correct

    is_correct = step1_answer == 'drag-t-rex' and step2_answer == 'drag-turtle' and step3_answer == 'drag-roll'
    
    # Set a message and possibly modify the lesson dictionary if needed
    if is_correct:
        flash('You got it right! Great job!', 'success')
    else:
        flash('Incorrect order. Try again.', 'danger')

    # Re-render the safety.html with the current lesson data
    return redirect(url_for('safety', lesson_id=lesson_id))

@app.route('/climbing_types')
def climbing_types_index():
    # Redirect to the first lesson of Climbing Types
    return redirect(url_for('climbing_types', lesson_id="1"))

@app.route('/climbing_types/<lesson_id>')
def climbing_types(lesson_id):
    lesson = climbing_types_lessons.get(lesson_id)
    if lesson is None:
        return redirect(url_for('home'))

    previous_lesson = lesson.get('previous_lesson')
    previous_lesson_url = url_for('home') if previous_lesson == "home" else url_for('climbing_types', lesson_id=previous_lesson)

    next_lesson = lesson.get('next_lesson')
    next_lesson_url = url_for('climbing_types', lesson_id=next_lesson)

    return render_template('climbing_types.html', lesson=lesson, previous_lesson_url=previous_lesson_url, next_lesson_url=next_lesson_url)


@app.route('/climbing_types/<lesson_id>/submit_quiz', methods=['POST'])
def submit_climbing_quiz(lesson_id):
    selected_option = request.form['quizAnswer']
    lesson = climbing_types_lessons.get(lesson_id, {})
    
    # Check if the selected answer is correct
    is_correct = selected_option == lesson.get('correct_answer')
    
    if is_correct:
        flash('Correct answer!', 'success')
    else:
        flash('Incorrect answer. Try again.', 'danger')
    
    return redirect(url_for('climbing_types', lesson_id=lesson_id))

@app.route('/grading_systems')
def grading_systems_index():
    # Redirect to the first lesson of Grading Systems
    return redirect(url_for('grading_systems', lesson_id="1"))

@app.route('/grading_systems/<lesson_id>')
def grading_systems(lesson_id):
    lesson = grading_systems_lessons.get(lesson_id)
    if lesson is None:
        return redirect(url_for('home'))

    previous_lesson = lesson.get('previous_lesson')
    previous_lesson_url = url_for('home') if previous_lesson == "home" else url_for('grading_systems', lesson_id=previous_lesson)

    next_lesson = lesson.get('next_lesson')
    next_lesson_url = url_for('grading_systems', lesson_id=next_lesson)

    return render_template('grading_systems.html', lesson=lesson, previous_lesson_url=previous_lesson_url, next_lesson_url=next_lesson_url)

@app.route('/grading_systems/<lesson_id>/submit_quiz', methods=['POST'])
def submit_grading_quiz(lesson_id):
    selected_option = request.form['quizAnswer']
    lesson = grading_systems_lessons.get(lesson_id, {})
    
    # Check if the selected answer is correct 
    is_correct = selected_option == lesson.get('correct_answer')
    
    if is_correct:
        flash('Correct answer!', 'success')
    else:
        flash('Incorrect answer. Try again.', 'danger')
    
    return redirect(url_for('grading_systems', lesson_id=lesson_id))

# Routes for handling the quiz page
user_answers = { # reset answers if retake quiz
            1: "",
            2: "",
            3: "",
            4: "",
            5: ""
        } 
@app.route('/reset_quiz')
def reset_quiz():
    global user_answers
    user_answers = {1: "", 2: "", 3: "", 4: "", 5: ""}
    return redirect(url_for('quiz', quiz_num="0"))

@app.route('/quiz')
def quiz_index():
    # Redirect to the start page of quiz
    if user_answers[5]:
        return redirect(url_for('view_result'))
    return redirect(url_for('quiz', quiz_num="0"))

@app.route('/quiz/<quiz_num>', methods=['GET', 'POST'])
def quiz(quiz_num):        
    if quiz_num != "0" and quiz_num != "1":
        answer = request.form.get('answer')
        if not user_answers[int(quiz_num) - 1]:
            user_answers[int(quiz_num) - 1] = answer
            print(user_answers)

    if quiz_num == "6":
        print("calculating score...")
        correct = 0
        for question_number, user_answer in user_answers.items():
            # Convert question_number to string to match quiz_data keys
            question_key = str(question_number)
            if question_key in quiz_data and quiz_data[question_key]["correct_answer"] == user_answer:
                print(question_key)
                quiz_data[question_key]["correct_answer"]
                print(user_answer)
                correct += 1  # Increment score for each correct answer
        print(correct)
        message = f"Congratulation! You got {correct} correct out of 5!"
        quiz_data["6"]["title"] = message

    quiz_question = quiz_data.get(quiz_num)
    return render_template('quiz.html', data=quiz_question)

results = {}
@app.route('/view_result', methods=['GET'])
def view_result():
    for key, value in user_answers.items():
        question = quiz_data[str(key)]
        is_correct = value in question['correct_answer'] if isinstance(question['correct_answer'], list) else value == question['correct_answer']
        results[key] = {
            'question': question['title'],
            'options': question['options'],
            'user_answer': value,
            'correct_answer': question['correct_answer'],
            'is_correct': is_correct,
            'media': question.get('media')  # Include media if available
        }
    return render_template('view_result.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug = True)
