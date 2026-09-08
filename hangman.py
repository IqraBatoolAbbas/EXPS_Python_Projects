import random
# 1. Words ki list aur maximum wrong attempts definition
word_list = ["python", "coding", "laptop", "mobile", "school"]
secret_word = random.choice(word_list)  # List me se random word select karega
max_attempts = 6
wrong_guesses = 0
guessed_letters = []

print(" HANGMAN GAME IN PYTHON ")
print("Word guess karein! Aapke paas total 6 wrong guesses hain.\n")

# 2. Main Game Loop
while wrong_guesses < max_attempts:
    # Word ka current state display karna (e.g., p _ t _ o _)
    display_word = ""
    for letter in secret_word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "

    print("Word:", display_word)
    print(f"Remaining attempts: {max_attempts - wrong_guesses}")
    print(f"Guessed letters: {', '.join(guessed_letters)}")

    # Check: Agar saare letters guess ho gaye hain to Player Jeet gaya!
    if "_" not in display_word:
        print("\n🎉 MUBARAK HO! Aap jeet gaye! Secret word tha:", secret_word)
        break

    # 3. User se Input lena
    guess = input("\nEk letter guess karein: ").lower()

    # Input Validation (Check karna ke input valid letter ho)
    if len(guess) != 1 or not guess.isalpha():
        print("❌ Please sirf ek single letter enter karein!\n")
        continue

    if guess in guessed_letters:
        print("⚠️ Aap yeh letter pehle hi guess kar chuke hain!\n")
        continue

    # Letter ko guessed_letters list me add karna
    guessed_letters.append(guess)

    # 4. Check karna ke letter secret word me hai ya nahi
    if guess in secret_word:
        print("✅ Sahi guess!\n")
    else:
        wrong_guesses += 1
        print("❌ Galat guess!\n")

# Agar attempts khatam ho jayein
if wrong_guesses == max_attempts:
    print("\n💀 Game Over! Aapke attempts khatam ho gaye.")
    print("Secret word tha:", secret_word)