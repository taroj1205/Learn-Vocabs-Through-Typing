import pygame
from random_word import RandomWords
from datetime import datetime
import os
from googletrans import Translator
import aiohttp
import asyncio
import pyttsx3

# Voice
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 0.9)
voices = engine.getProperty('voices')
time_to_wait = 200

random_word = RandomWords()
word = random_word.get_random_word()
fontColor_history = (150, 150, 150)     # (190, 190, 190)
fontColor_white = (255, 255, 255)
fontColor_plus = (31, 215, 85)
fontColor_minus = (255, 0, 0)
fontColor_typed = (43, 43, 43)
fontColor_remain = (255, 255, 255)
clock = pygame.time.Clock()
translator = Translator()
font_size_word = 100

# Accuracy
correct = 0
wrong = 0

pygame.init()
# Set the window dimensions
window_width = 1800
window_height = 800
# Create the window
window = pygame.display.set_mode((window_width, window_height))
# Set the background color
window.fill((13, 16, 17))
# Set the window title
pygame.display.set_caption('英単語が学べるタイピングゲーム')

txt_data = 'data.txt'
txt_words = 'words.txt'
txt_accuracy = 'accuracy.txt'

if not os.path.exists('data'):
    folder_name = 'data'
    os.makedirs(folder_name)
if os.path.exists('data\\' + txt_data):
    with open('data\\' + txt_data, 'r', encoding='utf-8') as f:
        count, score = f.read().split(',')
        count = int(count)
        score = int(score)
if os.path.exists('data\\' + txt_words):
    with open('data\\' + txt_words, 'r', encoding='utf-8') as f:
        words = f.read().split(',')
        wordsList = words
        # print(wordsList)

if os.path.exists('data\\' + txt_accuracy):
    with open('data\\' + txt_accuracy, 'r', encoding='utf-8') as f:
        correct,wrong = f.read().split(',')
        correct = int(correct)
        wrong = int(wrong)

else:
    with open('data\\' + txt_words, 'w', encoding='utf-8') as f:
        # Write to the file
        wordsList = []
        f.write('')
    with open('data\\' + txt_data, 'w', encoding='utf-8') as f:
        # Write to the file
        count = 0
        score = 0
        f.write(f"{count},{score}")
    with open('data\\' + txt_accuracy, 'w', encoding='utf-8') as f:
        correct = int(correct)
        wrong = int(wrong)
        f.write(f"{correct},{wrong}")


def count_score():
    # print(f"score: {score}")
    show_count = font_count.render(f"Words: {count}", True, fontColor_white)
    if score == 0:
        show_score = font_count.render(f"{score}", True, fontColor_white)
    elif score < 0:
        show_score = font_count.render(f"{score}", True, fontColor_minus)
    elif score > 0:
        show_score = font_count.render(f"{score}", True, fontColor_plus)
    else:
        show_score = font_count.render("error", True, 167, 0, 0)
    # Create a rect for the text surface and center it in the window
    text_rect_count = show_count.get_rect()
    text_rect_score = show_score.get_rect()
    # Display location
    text_rect_count.center = (window_width / 2, window_height / 2 + 120)
    text_rect_score.center = (window_width / 2, 20)
    # Display the letters
    window.blit(show_count, text_rect_count)
    window.blit(show_score, text_rect_score)
    display_accuracy(correct,wrong)


def display_accuracy(correct,wrong):
    if correct == 0 and wrong == 0:
        show_accuracy = font_count.render("Start Typing", True, fontColor_plus)
    else:
        if correct == 0:
            accuracy = 0
        elif wrong == 0:
            accuracy = 100
        else:
            accuracy = round((int(correct)/int(wrong+correct))*100,1)
        if accuracy >= 50:
            show_accuracy = font_count.render(f"{accuracy}%", True, fontColor_plus)
        elif accuracy <= 0:
            show_accuracy = font_count.render("0%", True, fontColor_minus)
        else:
            show_accuracy = font_count.render(f"{accuracy}%", True, fontColor_minus)
    # Create a rect for the text surface and center it in the window
    text_rect_accuracy = show_accuracy.get_rect()
    # Display location
    text_rect_accuracy.center = (window_width / 2, window_height - 20)
    # Display the letters
    window.blit(show_accuracy, text_rect_accuracy)

font_count = pygame.font.Font("Consolas.ttf", 20)
history_font = pygame.font.Font("NotoSansJP-Regular.otf", 20)
count_score()
display_accuracy(correct,wrong)

async def translate_async(word: str, src: str, dest: str) -> str:
    async with aiohttp.ClientSession() as session:
        # Set up proxy if necessary
        async with session.get(f"https://translate.google.com/translate_a/single?client=gtx&sl={src}&tl={dest}&dt=t&q={word}") as resp:
            data = await resp.json()
            return data[0][0][0]


async def main():
    font_size_word = 150
    src = 'en'
    dest = 'ja'
    translation = await translate_async(word, src, dest)
    display_remaining(font_size_word, translation)
    count_score()
    display_history()
    pygame.display.update()
    engine.setProperty('voice', voices[2].id)
    engine.say(translation)
    engine.runAndWait()
    pygame.time.wait(time_to_wait)
    window.fill((13, 16, 17))
    wordsList.append(f"{word[:counter]} ({translation})")


def display_history():
    if len(wordsList) != 0:
        while "" in wordsList:
            wordsList.remove("")
    history_height = 10
    for i in range(len(wordsList)-1, -1, -1):
        historyList = wordsList[i]

        if i == len(wordsList) - 1:
            historyList += " <"
        # Create a new text object with the updated alpha value
        history_text = history_font.render(historyList, True, fontColor_history)
        # Get the rect for the remaining letters
        history_rect = history_text.get_rect()
        # Offset the rect for the remaining letters so that it is positioned to left
        history_rect.left = 20
        # Position rect to the top
        history_rect.top = history_height
        # Offset the rect for the remaining letters so that it is positioned correctly
        history_height += 20
        # Display the remaining letters
        window.blit(history_text, history_rect)

# Choose a font and render the word as a surface
font = pygame.font.Font("Consolas.ttf", font_size_word)
text = font.render(word, True, fontColor_white)
# Create a rect for the text surface and center it in the window
text_rect = text.get_rect()
text_rect.center = (window_width / 2, window_height / 2)
# Blit the text surface to the window
window.blit(text, text_rect)
display_history()
# Update the display
pygame.display.update()

# Set the counter to 0
counter = 0

# Initialize the typed_text and typed_rect variables to empty values
typed_text = ""
typed_rect = pygame.Rect(0, 0, 0, 0)

# Run the game loop
running = True

def show_the_word(word):
    # Choose a font and render the word as a surface
    font_size_word = 130
    translation = word
    display_history()
    count_score()
    display_remaining(font_size_word, translation)
    pygame.display.update()
    window.fill((13, 16, 17))
    pygame.mixer.music.load('決定ボタンを押す1.mp3')
    pygame.mixer.music.play()
    pygame.time.wait(time_to_wait)
    engine.setProperty('voice', voices[0].id)
    engine.say(word)
    engine.runAndWait()
    asyncio.run(main())


def update_typed():
    # Split the word into two parts: the typed letters and the letters that have not been typed yet
    typed_letters = word[:counter]
    # Choose a smaller font size for the typed letters
    small_font = pygame.font.Font("Consolas.ttf", 50)
    # Render the typed letters with the smaller font size
    typed_text = small_font.render(typed_letters, True, fontColor_typed)
    # Get the rect for the typed letters
    typed_rect = typed_text.get_rect()
    # Display location
    typed_rect.center = (window_width / 2, window_height / 2 - 70)
    # Display the typed letters
    window.blit(typed_text, typed_rect)


def update_remain():
    # Split the word into two parts: the typed letters and the letters that have not been typed yet
    remaining_letters = word[counter:]
    # Render the remaining letters with the original font size
    remaining_text = font.render(remaining_letters, True, fontColor_remain)
    # Get the rect for the remaining letters
    remaining_rect = remaining_text.get_rect()
    # Offset the rect for the remaining letters so that it is positioned correctly
    remaining_rect.center = (window_width / 2, window_height / 2)
    # Display the remaining letters
    window.blit(remaining_text, remaining_rect)
    display_history()


def update_word():
    if counter != len(word):
        count_score()

    update_typed()
    update_remain()
    # Update the display
    pygame.display.update()
    # print("Updated word")


def update_display():
    text = font.render(word, True, fontColor_white)
    # Create a rect for the text surface and center it in the window
    text_rect = text.get_rect()
    text_rect.center = (window_width / 2, window_height / 2)
    # Blit the text surface to the window
    window.blit(text, text_rect)


    # print(f"Count: {count}")
    # (f"Score: {score}")
    count_score()


def display_remaining(font_size_word, translation):
    remaining_text = pygame.font.Font("NotoSansJP-Regular.otf", font_size_word).render(translation, True, fontColor_white)
    remaining_rect = remaining_text.get_rect()
    remaining_rect.center = (window_width / 2, window_height / 2)
    window.blit(remaining_text, remaining_rect)

while running:
    # Set the background color
    window.fill((13, 16, 17))
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                # dd/mm/YY H:M:S
                dt_string = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                file_name = f'data {str(dt_string)} (backup).txt'
                with open('data\\' + file_name, 'w') as f:
                    f.write(f"{str(count)},{str(score)}")
                with open('data\\' + txt_data, 'w') as f:
                    # Write to the file
                    score = 0
                    f.write(f"{count},{score}")
                file_name = f'words {str(dt_string)} (backup).txt'
                with open('data\\' + file_name, 'w', encoding="utf-8") as f:
                    # Remove empty in array
                    while "" in wordsList:
                        wordsList.remove("")
                    # Change ['word'] to word
                    typed_words = ''.join(f'{str(x)},' for x in wordsList)
                    # Write to the file
                    f.write(typed_words)
                with open('data\\' + txt_words, 'w') as f:
                    f.write(" ")
                    wordsList = []
                file_name = f'accuracy {str(dt_string)} (backup).txt'
                with open('data\\' + file_name, 'w', encoding="utf-8") as f:
                    f.write(f"{correct},{wrong}")
                with open('data\\' + txt_accuracy, 'w', encoding='utf-8') as f:
                    correct = 0
                    wrong = 0
                    f.write(f"{correct},{wrong}")
                counter = 0
                count = 0
                # print(f"Count: {count}")
                update_display()
                # Update the display
                pygame.display.update()
            if keys[pygame.K_LALT]:
                pass
            else:
                if event.unicode.lower() == word[counter].lower():
                    # print('Correct!')
                    # Increment the counter
                    counter += 1
                    score += 1
                    correct += 1
                    fontColor_remain = (31, 215, 85)
                    # print(f"+1 counter: {counter}")
                    # print(f"+1 score: {score}")
                    if counter == len(word):
                        fontColor_remain = (255, 255, 255)
                        show_the_word(word)
                        word = random_word.get_random_word()
                        counter = 0
                        count += 1
                        update_typed()
                        update_display()
                        # Update the display
                        pygame.display.update()
                    # display_history()
                    update_word()
                    count_score()
                elif keys[pygame.K_ESCAPE] == False:
                    fontColor_remain = (255, 0, 0)
                    score -= 1
                    wrong += 1
                    # display_history()
                    count_score()
                    update_word()
                    # Update the display
                    pygame.display.update()
                    # print(f"-1 score: {score}")
        if event.type == pygame.QUIT:
            # Open the file in write mode
            with open('data\\' + txt_data, 'w', encoding='utf-8') as f:
                # Write to the file
                f.write(f"{str(count)},{str(score)}")
            if len(wordsList) != 0:
                with open('data\\' + txt_words, 'w', encoding='utf-8') as f:
                    # print(f"Typed words: {wordsList}")
                    # Remove empty in array
                    while "" in wordsList:
                        wordsList.remove("")
                    # Change ['word'] to word
                    typed_words = ''.join(f'{str(x)},' for x in wordsList)
                    # print(f"Typed words: {typed_words}")
                    # print(typed_words)
                    # Write to the file
                    f.write(typed_words)
            with open('data\\' + txt_accuracy, 'w', encoding='utf-8') as f:
                f.write(f"{correct},{wrong}")
            running = False
