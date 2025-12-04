
import gradio as gr
from soundness_check import correct_uv_with_highlights
import os


def load_test_text_content():
    try:
        if not os.path.exists('test_texts.txt'):
            return "Вставте ваш текст тут. Файл 'test_texts.txt' не знайдено."

        with open('test_texts.txt', 'r', encoding='utf-8') as f:
            content_blocks = f.read().split('\n\n')
            if content_blocks:
                parts = content_blocks[0].split('\n', 1)
                if len(parts) > 1:
                    return parts[1].strip()
        return "Вставте ваш текст тут..."
    except Exception:
        return "Вставте ваш текст тут..."


def process_text(text):
    if not text.strip():
        return "", ""

    corrected, highlighted = correct_uv_with_highlights(text)


    highlighted = highlighted.replace(
        '<span class="mistake"',
        '<span style="background:#ffebee;color:#c62828;'
        'border-bottom:2px dashed #ef9a9a;padding:0 4px 1px;'
        'border-radius:4px;font-weight:500;cursor:help;display:inline;'
        'animation:pulse 1.8s infinite;"'
    )

    styled_html = f"""
    <style>
    @keyframes pulse {{
        0%, 100% {{ background-color: #ffebee; }}
        50% {{ background-color: #ffd5d5; }}
    }}
    </style>
    {highlighted}
    """

    return styled_html, corrected


input_box = gr.Textbox(
    lines=12,
    label="Оригінальний текст",
    value=load_test_text_content(),
    placeholder="Вставте текст для аналізу..."
)

output_html = gr.HTML(label="Оригінал з підсвіченими помилками")

output_corrected = gr.Textbox(
    lines=12,
    label="✅ Виправлений текст",
    interactive=False
)


iface = gr.Interface(
    fn=process_text,
    inputs=input_box,
    outputs=[output_html, output_corrected],
    title="Коректор Вживання прийменників і префіксів у, в",
    description="Автоматичне виправлення чергування **у/в** згідно з правилами милозвучності.",
    submit_btn="Виправити 'У/В'",
    clear_btn="Очистити",

    examples=[
        [
            "У осінньому парку я побачив людину у зеленому плащі. "
            "Увечері ми зібралися в будинку друзів, але в кімнаті було занадто темно. "
            "В відповідь пролунало лише тихе бурмотіння в темряві."
        ],
        [
            "У школі в учнів часто виникають труднощі в опануванні правил милозвучності. "
            "В українській мові в вживанні прийменників багато нюансів. "
            "Учитель наголосив на потребі тренувати чуття мови в усному мовленні."
        ],
        [
            "Ми стояли в черзі в музей, але в воротах утворилося скупчення людей. "
            "Усередині будівлі було тепло, і в всіх одразу покращився настрій."
        ],
        [
            "У нашому місті відкрили новий парк в районі набережної. "
            "В вихідні там завжди багато людей, які гуляють в алеях та в скверах поблизу."
        ],
        [
            "У автобусі в водія грала тиха музика. "
            "В вікні мерехтіли вогні вулиць, що тягнулися удалечінь. "
            "У повітрі відчувалася прохолода осіннього ранку."
        ]
    ]
)


if __name__ == "__main__":
    print("✅ Запуск інтерфейсу…")
    iface.launch()

