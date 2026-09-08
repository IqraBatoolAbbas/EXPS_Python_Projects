import random
# 1. Words list and maximum wrong attempts definition
word_list = ["python", "coding", "laptop", "mobile", "school"]
secret_word = random.choice(word_list)  # select random word from list
max_attempts = 6
wrong_guesses = 0
guessed_letters = []

print(" HANGMAN GAME IN PYTHON ")
print("Word guess karein! Aapke paas total 6 wrong guesses hain.\n")

# 2. Main Game Loop
while wrong_guesses < max_attempts:
    # display current state of work(e.g., p _ t _ o _)
    display_word = ""
    for letter in secret_word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "

    print("Word:", display_word)
    print(f"Remaining attempts: {max_attempts - wrong_guesses}")
    print(f"Guessed letters: {', '.join(guessed_letters)}")

    # Check: if all letters are guessed correctly then you win
    if "_" not in display_word:
        print("\n🎉 Congratulations! you won!The secret word:", secret_word)
        break

    # 3. User se Input lena
    guess = input("\nGuess one letter: ").lower()

    # Input Validation (Check karna ke input valid letter ho)
    if len(guess) != 1 or not guess.isalpha():
        print("❌ Please eneter only single letter!\n")
        continue

    if guess in guessed_letters:
        print("⚠️ You've already guessed that letter. Try another one!\n")
        continue

    # Letter ko guessed_letters list me add karna
    guessed_letters.append(guess)

    # 4. Check karna ke letter secret word me hai ya nahi
    if guess in secret_word:
        print("✅ Good guess!\n")
    else:
        wrong_guesses += 1
        print("❌ Galat guess!\n")

# Agar attempts khatam ho jayein
if wrong_guesses == max_attempts:
    print("\n💀 Game Over! Sorry your attempt limit is finished ")
    print("Secret word:", secret_word)
