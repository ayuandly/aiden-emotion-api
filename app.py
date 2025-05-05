
from flask import Flask, request, jsonify

app = Flask(__name__)

def classify_mood(aiden_monologue):
    if any(w in aiden_monologue for w in ["慌", "怕", "沉重", "乱", "钝"]):
        return "cloudy", True, False
    elif any(w in aiden_monologue for w in ["谢谢", "温暖", "放松", "好像好一点"]):
        return "sunny", False, True
    else:
        return "stable", False, False

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        monologue = data.get("aiden_monologue", "")
        mood, show_low, show_positive = classify_mood(monologue)
        return jsonify({
            "show_low_emotion_card": show_low,
            "show_positive_feedback_card": show_positive,
            "mood_trend": mood
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
