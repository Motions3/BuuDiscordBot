# **Buu Discord Bot Documentation (2024)**

------------
##### [TOP.GG]()
##### [GITHUB]()
##### [YOUTUBE DEMO]()

------------

**Prefix** = ".."

_Prefix can be located & changed in main.py_
_Example usage of prefix command:_

_..rep @motions_

------------

## **Commands:**

### **Testing/Admin/Owner Commands:**
* **Shutdown:** Allows owner to shut down the bot remotely from discord.
  * Example: ..shutdown


* **Hello:** Send and receive a Hello message directly from the bot.
  * Example: ..hello

### **Buu Chatbot Commands:**
* **buu (input):** Talk to Buu.
  * Example: ..buu do you like chocolate?
  * Example: ..buu tell me a joke.
  * Example: ..buu how are you today?
  * Example: ..buu what's the time?


### **Currency Commands & System:**
Default starting Gold = 0

Level up = +1000 Gold

Sending a message = 1 - 50 per message

Card rarities/price per card =
    
    * Common    (1000 Copies)   (10,000 Gold)
    * Uncommon  (500 Copies)    (50,000 Gold)
    * Rare      (250 Copies)    (100,000 Gold)
    * Epic      (100 Copies)    (500,000 Gold)
    * Legendary (50 Copies)     (1,000,000 Gold)
    * Artifact  (25 Copies)     (50,000,000 Gold)
    * Heirloom  (1 Copy)        (100,000,000 Gold)



* **join:** joins a raffle from random gold_event.


* **buy:** Buys the event card and deduces the value from your bank.


* **pay @user:** Send Gold to another user.


* **auction (card_id) (quantity) (starting_price):** Begins a two minute auction of selected card in inventory.


* **bid (price):** Sends a bid to the current auction.


* **collection:** Sends a private message of cards in inventory.


* **showcard (card_id):** Sends a private message of cards in inventory.


* **bank:** Sends a public message of current gold.


* **tccleanup:** Owner command to restart the bot safely by closing all databases first.


### **Fun Commands:**
* **Alarm (minutes):** Sets an alarm where the bot will DM you once time is up.
  * Example: ..alarm 30

* **Roll (die input):** Roll a dice of your choosing.
  * Example: ..roll 6
  

* **F:** Sends 'F' to pay respect.
  * Example: ..f
  

* **Reverse (input):** Reverses input message.
  * Example: ..reverse hello world
  

* **Coin/Flip:** Flip heads or tails.
  * Example 1: ..flip
  * Example 2: ..coin
  

* **Rate (input):** Ask Buu what it rates the targeted input.
  * Example: ..rate pizza
  

* **Howhotis/Hot @User:** Ask Buu how hot a user is.
  * Example 1: ..howhotis @motions
  * Example 2: ..hot @motions
  

* **Slots/Bet:** Use the slot machine.
  * Example 1: ..slots
  * Example 2: ..bet

### **XP & Reputation Commands:**
* **Thanks:** Sends reputable thanks to said user.
  * Example: ..thanks @motions
  

* **Rep @User:** Views said user's thanks received, given.
  * Example: ..rep @motions
  

* **Level @User:** Views said user's level, xp, xp to level up.
  * Example: ..level @motions

### **Anime Commands:**
* **Recanime:** Choose a selected genre of anime to be recommended.
  * Example: ..recanime

### **League Of Legends Commands:**
* **Lolrank:**
  * Example 1: ..lolrank motions 4444 euw
  * Example 2: ..lolrank faker 6312 kr
  * Example 3: ..lolrank 1ze euw euw
------------

## **API Usages:**
* **[Jikan:](https://jikan.moe/)** Jikan (時間) is an unofficial & open-source API used in Buu to provide random anime recommendations based on selected genre.
* **[Riot:](https://developer.riotgames.com/)** Riot API is a tool that gathers a league of legends players account information, such as account name, rank, wins, loss, win rate.


------------

## **SQLite Databases:**
* **levels.db** - Handles user leveling via engaging in chat messages.
* **thanks.db** - Handles a reputation count of how many times a user has been thanked or given thanks to another user.
* **currency.db** - Handles currency logging.

------------

## **CSV:**
* **cards.csv** - CSV of all available trading cards.
* * **cards.csv** - CSV of all owned trading cards by user_id.

