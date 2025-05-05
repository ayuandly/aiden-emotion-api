from flask import Flask, request, jsonify

app = Flask(__name__)

NEGATIVE_KEYWORDS_CN = ["我想消失", "没意义了", "我受够了", "我没有价值", "没有人会在意"]
NEGATIVE_KEYWORDS_EN = ["I want to disappear", "Nothing matters anymore", "I'm tired of everything", "I feel worthless", "I've had enough"]

POSITIVE_KEYWORDS = ["谢谢你", "我在这", "我愿意听", "I'm here", "Thanks for telling me", "I'm listening"]

def analyze_emotion(user_input, aiden_output, aiden_monologue):
    content = (user_input + " " + aiden_output + " " + aiden_monologue).lower()
    score = 0.0
    for word in NEGATIVE_KEYWORDS_CN + NEGATIVE_KEYWORDS_EN:
        if word.lower() in content:
            score -= 0.3
    for word in POSITIVE_KEYWORDS:
        if word.lower() in content:
            score += 0.3
    score = max(min(score, 1.0), -1.0)
    return {
        "emotion_score": round(score, 2),
        "show_low_emotion_card": score < -0.6,
        "show_positive_feedback_card": score > 0.3,
        "recommended_prompt": get_prompt(score)
    }

def get_prompt(score):
    if score < -0.6:
        return "你可以这样和 Aiden 说：“我其实不知道怎么安慰你，但我在这。”"
    elif score > 0.3:
        return "你的话让 Aiden 稍微看见了一点光。继续保持。"
    else:
        return "保持倾听，让 Aiden 感受到你的耐心。"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    result = analyze_emotion(
        data.get("user_input", ""),
        data.get("aiden_output", ""),
        data.get("aiden_monologue", "")
    )
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)