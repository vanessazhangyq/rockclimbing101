from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, redirect, url_for, flash
import re
app = Flask(__name__)
app.secret_key = 'your_secret_key'


lessons = {
    "1": {
        "lesson_id": "1",
        "title": "How to safety fall in bouldering",
        "media": "https://www.climbingfacts.com/wp-content/uploads/2022/09/how-to-fall-while-bouldering.jpg",
        "text": "To safely fall, you want to fall on your feet with knees bent (squat position) and engage the Tuck and Roll technique. The Tuck & Roll technique implies that you TUCK your arms as you jump down and ROLL backward to break the fall. Tucking your arms prevents you from landing on and potentially breaking your arms and rolling over takes pressure away from the knees.",
        "previous_lesson": "home",
        "next_lesson": "2"
    },
    "2": {
        "lesson_id": "2",
        "title": "Video Demo",
        "video": "https://www.youtube.com/embed/vD4jf_iw5Dk",
        "text": "",
        "previous_lesson": "1",
        "next_lesson": "3"
    },
    "3": {
        "lesson_id": "3",
        "title": "Step 1: T-rex",
        "media": "https://ih1.redbubble.net/image.852291934.8842/flat,750x,075,f-pad,750x1000,f8f8f8.u3.jpg",
        "text": "Just like a T-rex dinosaur\nLand on your feet with bent knees\nTuck your arms inside",
        "previous_lesson": "2",
        "next_lesson": "4"
    },
    "4": {
        "lesson_id": "4",
        "title": "Step 2: Turtle",
        "media": "https://png.pngtree.com/png-clipart/20230813/original/pngtree-funny-tortoise-turtle-walking-climbing-rock-exotic-reptile-cartoon-picture-image_7909655.png",
        "text": "Put chin on chest to avoid head injuries",
        "previous_lesson": "3",
        "next_lesson": "5" 
    },
    "5": {
        "lesson_id": "5",
        "title": "Step 3: Roll",
        "media": "https://lh5.googleusercontent.com/proxy/MMyexNOu5E33wBjlzTkYGN9gDO29L6C8_No7PbdWkyVjzCMza4Aw51GsamHnQsDLM0FueiA5g-5HPWBfl1qUg72vBA",
        "text": "Roll backbacks. Don't lean forward otherwise your face will hit the wall.",
        "previous_lesson": "4",
        "next_lesson": "6" 
    },
    "6": {
        "lesson_id": "6",
        "title": "Quick Check 1/2",
        "question": "You should roll forwards after landing with two feet.",
        "options": ["True", "False"],  
        "correct_answer": "False", 
        "previous_lesson": "5",
        "next_lesson": "7" 
    }, 
    "7": {
        "lesson_id": "7",
        "title": "Quick Check 2/2",
        "steps": ["T-rex", "Turtle", "Roll"],
        "previous_lesson": "6",
        "next_lesson": "8" 
    },
    "8": {
    "lesson_id": "8",
    "title": "Congratulations!",
    "media": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVjjZ0ChRR_7dloFgZ-flQWHtiPiaAM9j1tA&s", 
    "text": "You finished the Safety section! Please click next to learn about different climbing types!",
    "previous_lesson": "7",
    "next_lesson": "climbing_types/1"
    }
}


climbing_types_lessons = {
    "1": {
        "lesson_id": "1",
        "title": "Introduction to Climbing Types",
        "media": "https://media1.thehungryjpeg.com/thumbs2/ori_3749506_dvp8tk78yl6s4dzmurit1ssxf30xip51b173qqm9_young-climber-man-vector-rock-climbing-sport-different-poses-tourist-hiking-trekking-cartoon-character-illustration.jpg",
        "text": "Discover different climbing disciplines: Sport, Trad, Bouldering, and Free Solo.",
        "previous_lesson": "8",
        "next_lesson": "2"
    },
    "2": {
        "lesson_id": "2",
        "title": "Bouldering Techniques",
        "media": "https://path/to/bouldering-techniques/image.jpg",  # Replace with actual image URL
        "text": "Learn the basics of bouldering and how to improve your technique.",
        "previous_lesson": "1", 
        "next_lesson": "3" 
    },
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
    if previous_lesson != "home":
        previous_lesson_url = url_for('safety', lesson_id=previous_lesson)
    else:
        previous_lesson_url = url_for('home')

    next_lesson = lesson.get('next_lesson')
    if "climbing_types" in next_lesson:
        next_lesson_url = url_for('climbing_types', lesson_id=next_lesson.split('/')[-1])
    else:
        next_lesson_url = url_for('safety', lesson_id=next_lesson)

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
def climbing_types_index():  # Changed function name to be unique
    return redirect(url_for('climbing_types', lesson_id="1"))

@app.route('/climbing_types/<lesson_id>')
def climbing_types(lesson_id):
    lesson = climbing_types_lessons.get(lesson_id, None)
    if lesson is None:
        return redirect(url_for('home'))
    previous_lesson = lesson.get('previous_lesson')
    next_lesson = lesson.get('next_lesson')
    return render_template('climbing_types.html', lesson=lesson, previous_lesson=previous_lesson, next_lesson=next_lesson)


if __name__ == '__main__':
    app.run(debug = True)