# import all necessary libraries
import os
import csv
import nltk
import torch
from nltk.tokenize import sent_tokenize
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from torch.nn.functional import softmax

# used torch instead of numpy in this case

nltk.download("punkt")

# initialize the RoBERTa model (training model using to acquire sentiment analysis) and tokenizer from the Hugging Face library
model_name = "cardiffnlp/twitter-roberta-base-sentiment"  # specific model name
tokenizer = RobertaTokenizer.from_pretrained(model_name)
model = RobertaForSequenceClassification.from_pretrained(model_name)


def get_sentiment(text):
    # tokenize the text to split up the words in the text provided as a parameter, referred to the websites above
    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, padding=True, max_length=512
    )

    # gets the sentiment raw score using the RoBERTa model, referred to the websites above
    with torch.no_grad():
        output = model(**inputs).logits

    # get the probabilities with a softmax function to ensure the sum of the probabilities is 1, referred to the websites above and the one below
    probs = softmax(output, dim=-1)

    # create lists to store labels and confidences for each sentiment; define labels
    labels = []
    confidences = []
    sentiment_labels = ["Negative", "Neutral", "Positive"]

    # loop through the sentiment labels and get their corresponding confidence levels
    for label_index, label in enumerate(sentiment_labels):
        confidence = probs[0][label_index].item()
        labels.append(label)
        confidences.append(confidence)

    # return lists of sentiment labels and their corresponding confidences
    return labels, confidences


# list of stories (replace these with your actual stories)
stories = [
    # FIRST STORY: molly whuppie
    """Once upon a time there was a man and a wife had too many children, and they could not get meat for them, so they took the three youngest and left them in a wood. 
They travelled and travelled and could see never a house. It began to be dark, and they were hungry. At last they saw a light and made for it; it turned out to be a house. They knocked at the door, and a woman came to it, who said: “What do you want?” They said: “Please let us in and give us something to eat.” The woman said: “I can't do that, as my man is a giant, and he would kill you if he comes home.” They begged hard. “Let us stop for a little while,” said they, “and we will go away before he comes.” So she took them in, and set them down before the fire, and gave them milk and bread; but just as they had begun to eat a great knock came to the door, and a dreadful voice said:
“Fee, fie, fo, fum,
I smell the blood of some earthly one.
Who have you there wife?” “Eh,” said the wife, “it's three poor lassies cold and hungry, and they will go away. Ye won't touch 'em, man.” He said nothing, but ate up a big supper, and ordered them to stay all night. Now he had three lassies of his own, and they were to sleep in the same bed with the three strangers.
The youngest of the three strange lassies was called Molly Whuppie, and she was very clever. She noticed that before they went to bed the giant put straw ropes round her neck and her sisters', and round his own lassies' necks he put gold chains. So Molly took care and did not fall asleep, but waited till she was sure every one was sleeping sound. Then she slipped out of the bed, and took the straw ropes off her own and her sisters' necks, and took the gold chains off the giant's lassies. She then put the straw ropes on the giant's lassies and the gold on herself and her sisters, and lay down.
And in the middle of the night up rose the giant, armed with a great club, and felt for the necks with the straw. It was dark. He took his own lassies out of bed on to the floor, and battered them until they were dead, and then lay down again, thinking he had managed fine. Molly thought it time she and her sisters were out of that, so she wakened them and told them to be quiet, and they slipped out of the house. They all got out safe, and they ran and ran, and never stopped until morning, when they saw a grand house before them. It turned out to be a king's house: so Molly went in, and told her story to the king. He said: “Well, Molly, you are a clever girl, and you have managed well; but, if you would manage better, and go back, and steal the giant's sword that hangs on the back of his bed, I would give your eldest sister my eldest son to marry.” Molly said she would try.
So she went back, and managed to slip into the giant's house, and crept in below the bed. The giant came home, and ate up a great supper, and went to bed. Molly waited until he was snoring, and she crept out, and reached over the giant and got down the sword; but just as she got it out over the bed it gave a rattle, and up jumped the giant, and Molly ran out at the door and the sword with her; and she ran, and he ran, till they came to the “Bridge of one hair”; and she got over, but he couldn't, and he says, “Woe worth ye, Molly Whuppie! never ye come again.” And she says “Twice yet, carle,” quoth she, “I'll come to Spain.” So Molly took the sword to the king, and her sister was married to his son.
Well, the king he says: “Ye've managed well, Molly; but if ye would manage better, and steal the purse that lies below the giant's pillow, I would marry your second sister to my second son.” And Molly said she would try. So she set out for the giant's house, and slipped in, and hid again below the bed, and waited till the giant had eaten his supper, and was snoring sound asleep. She slipped out, and slipped her hand below the pillow, and got out the purse; but just as she was going out the giant wakened, and ran after her; and she ran, and he ran, till they came to the “Bridge of one hair,” and she got over, but he couldn't, and he said, “Woe worth ye, Molly Whuppie! never you come again.” “Once yet, carle,” quoth she, “I'll come to Spain.” So Molly took the purse to the king, and her second sister was married to the king's second son.
After that the king says to Molly: “Molly, you are a clever girl, but if you would do better yet, and steal the giant's ring that he wears on his finger, I will give you my youngest son for yourself.” Molly said she would try. So back she goes to the giant's house, and hides herself below the bed. The giant wasn't long ere he came home, and, after he had eaten a great big supper, he went to his bed, and shortly was snoring loud. Molly crept out and reached over the bed, and got hold of the giant's hand, and she pulled and she pulled until she got off the ring; but just as she got it off the giant got up, and gripped her by the hand, and he says: “Now I have catcht you, Molly Whuppie, and, if I had done as much ill to you as ye have done to me, what would ye do to me?”
Molly says: “I would put you into a sack, and I'd put the cat inside with you, and the dog aside you, and a needle and thread and a shears, and I'd hang you up upon the wall, and I'd go to the wood, and choose the thickest stick I could get, and I would come home, and take you down, and bang you till you were dead.”
“Well, Molly,” says the giant, “I'll just do that to you.”
So he gets a sack, and puts Molly into it, and the cat and the dog beside her, and a needle and thread and shears, and hangs her up upon the wall, and goes to the wood to choose a stick.
Molly she sings out: “Oh, if ye saw what I see.”
“Oh,” says the giant's wife, “what do ye see, Molly?”
But Molly never said a word but, “Oh, if ye saw what I see!”
The giant's wife begged that Molly would take her up into the sack till she would see what Molly saw. So Molly took the shears and cut a hole in the sack, and took out the needle and thread with her, and jumped down and helped, the giant's wife up into the sack, and sewed up the hole.
The giant's wife saw nothing, and began to ask to get down again; but Molly never minded, but hid herself at the back of the door. Home came the giant, and a great big tree in his hand, and he took down the sack, and began to batter it. His wife cried, “It's me, man;” but the dog barked and the cat mewed, and he did not know his wife's voice. But Molly came out from the back of the door, and the giant saw her, and he after her; and he ran and she ran, till they came to the “Bridge of one hair,” and she got over but he couldn't; and he said, “Woe worth you, Molly Whuppie! never you come again.” “Never more, carle,” quoth she, “will I come again to Spain.”
So Molly took the ring to the king, and she was married to his youngest son, and she never saw the giant again.""",
    # SECOND STORY: the story of the three bears
    """Once upon a time there were Three Bears, who lived together in a house of their own, in a wood. 
One of them was a Little, Small Wee Bear; and one was a Middle-sized Bear, and the other was a Great, Huge Bear. 
They had each a pot for their porridge, a little pot for the Little, Small, Wee Bear; and a middle-sized pot for the Middle Bear, and a great pot for the Great, Huge Bear. 
And they had each a chair to sit in; a little chair for the Little, Small, Wee Bear; and a middle-sized chair for the Middle Bear; and a great chair for the Great, Huge Bear. 
And they had each a bed to sleep in; a little bed for the Little, Small, Wee Bear; and a middle-sized bed for the Middle Bear; and a great bed for the Great, Huge Bear.
One day, after they had made the porridge for their breakfast, and poured it into their porridge-pots, they walked out into the wood while the porridge was cooling, that they might not burn their mouths, by beginning too soon to eat it. 
And while they were walking, a little old Woman came to the house. 
She could not have been a good, honest old Woman; for first she looked in at the window, and then she peeped in at the keyhole; and seeing nobody in the house, she lifted the latch. 
The door was not fastened, because the Bears were good Bears, who did nobody any harm, and never suspected that anybody would harm them. 
So the little old Woman opened the door, and went in; and well pleased she was when she saw the porridge on the table. 
If she had been a good little old Woman, she would have waited till the Bears came home, and then, perhaps, they would have asked her to breakfast; for they were good Bears—a little rough or so, as the manner of Bears is, but for all that very good-natured and hospitable. 
But she was an impudent, bad old Woman, and set about helping herself.
So first she tasted the porridge of the Great, Huge Bear, and that was too hot for her; and she said a bad word about that. 
And then she tasted the porridge of the Middle Bear, and that was too cold for her; and she said a bad word about that too. 
And then she went to the porridge of the Little, Small, Wee Bear, and tasted that; and that was neither too hot, nor too cold, but just right; and she liked it so well, that she ate it all up: but the naughty old Woman said a bad word about the little porridge-pot, because it did not hold enough for her.
Then the little old Woman sate down in the chair of the Great, Huge Bear, and that was too hard for her. 
And then she sate down in the chair of the Middle Bear, and that was too soft for her. 
And then she sate down in the chair of the Little, Small, Wee Bear, and that was neither too hard, nor too soft, but just right. 
So she seated herself in it, and there she sate till the bottom of the chair came out, and down she came, plump upon the ground. 
And the naughty old Woman said a wicked word about that too.
Then the little old Woman went upstairs into the bed-chamber in which the three Bears slept. 
And first she lay down upon the bed of the Great, Huge Bear; but that was too high at the head for her. 
And next she lay down upon the bed of the Middle Bear; and that was too high at the foot for her. 
And then she lay down upon the bed of the Little, Small, Wee Bear; and that was neither too high at the head, nor at the foot, but just right. 
So she covered herself up comfortably, and lay there till she fell fast asleep.
By this time the Three Bears thought their porridge would be cool enough; so they came home to breakfast. 
Now the little old Woman had left the spoon of the Great, Huge Bear, standing in his porridge.
“Somebody has been at my porridge!” said the Great, Huge Bear, in his great, rough, gruff voice. 
And when the Middle Bear looked at his, he saw that the spoon was standing in it too. 
They were wooden spoons; if they had been silver ones, the naughty old Woman would have put them in her pocket.
“Somebody has been at my porridge!” said the Middle Bear in his middle voice.
Then the Little, Small, Wee Bear looked at his, and there was the spoon in the porridge-pot, but the porridge was all gone.
“Somebody has been at my porridge, and has eaten it all up!” said the Little, Small, Wee Bear, in his little, small, wee voice.
Upon this the Three Bears, seeing that some one had entered their house, and eaten up the Little, Small, Wee Bear's breakfast, began to look about them. Now the little old Woman had not put the hard cushion straight when she rose from the chair of the Great, Huge Bear.
“Somebody has been sitting in my chair!” said the Great, Huge Bear, in his great, rough, gruff voice.
And the little old Woman had squatted down the soft cushion of the Middle Bear. 
“Somebody has been sitting in my chair!” said the Middle Bear, in his middle voice.
And you know what the little old Woman had done to the third chair.
“Somebody has been sitting in my chair and has sate the bottom out of it!” said the Little, Small, Wee Bear, in his little, small, wee voice.
Then the Three Bears thought it necessary that they should make farther search; so they went upstairs into their bedchamber. 
Now the little old Woman had pulled the pillow of the Great, Huge Bear, out of its place.
“Somebody has been lying in my bed!” said the Great, Huge Bear, in his great, rough, gruff voice.
And the little old Woman had pulled the bolster of the Middle Bear out of its place.
“Somebody has been lying in my bed!” said the Middle Bear, in his middle voice.
And when the Little, Small, Wee Bear came to look at his bed, there was the bolster in its place; and the pillow in its place upon the bolster; and upon the pillow was the little old Woman's ugly, dirty head,—which was not in its place, for she had no business there.
“Somebody has been lying in my bed,—and here she is!” said the Little, Small, Wee Bear, in his little, small, wee voice.
The little old Woman had heard in her sleep the great, rough, gruff voice of the Great, Huge Bear; but she was so fast asleep that it was no more to her than the roaring of wind, or the rumbling of thunder. 
And she had heard the middle voice, of the Middle Bear, but it was only as if she had heard some one speaking in a dream. 
But when she heard the little, small, wee voice of the Little, Small, Wee Bear, it was so sharp, and so shrill, that it awakened her at once. 
Up she started; and when she saw the Three Bears on one side of the bed, she tumbled herself out at the other, and ran to the window. 
Now the window was open, because the Bears, like good, tidy Bears, as they were, always opened their bedchamber window when they got up in the morning. 
Out the little old Woman jumped; and whether she broke her neck in the fall; or ran into the wood and was lost there; or found her way out of the wood, and was taken up by the constable and sent to the House of Correction for a vagrant as she was, I cannot tell. 
But the Three Bears never saw anything more of her.""",
    # THIRD STORY: the fish and the ring
    """Once upon a time, there was a mighty baron in the North Countrie who was a great magician that knew everything that would come to pass. 
So one day, when his little boy was four years old, he looked into the Book of Fate to see what would happen to him. 
And to his dismay, he found that his son would wed a lowly maid that had just been born in a house under the shadow of York Minster. Now the Baron knew the father of the little girl was very, very poor, and he had five children already. So he called for his horse, and rode into York; and passed by the father's house, and saw him sitting by the door, sad and doleful. So he dismounted and went up to him and said: “What is the matter, my good man?” And the man said: “Well, your honour, the fact is, I've five children already, and now a sixth's come, a little lass, and where to get the bread from to fill their mouths, that's more than I can say.”
“Don't be downhearted, my man,” said the Baron. “If that's your trouble, I can help you. I'll take away the last little one, and you wont have to bother about her.”
“Thank you kindly, sir,” said the man; and he went in and brought out the lass and gave her to the Baron, who mounted his horse and rode away with her. And when he got by the bank of the river Ouse, he threw the little, thing into the river, and rode off to his castle.
But the little lass didn't sink; her clothes kept her up for a time, and she floated, and she floated, till she was cast ashore just in front of a fisherman's hut. There the fisherman found her, and took pity on the poor little thing and took her into his house, and she lived there till she was fifteen years old, and a fine handsome girl.
One day it happened that the Baron went out hunting with some companions along the banks of the River Ouse, and stopped at the fisherman's hut to get a drink, and the girl came out to give it to them. They all noticed her beauty, and one of them said to the Baron: “You can read fates, Baron, whom will she marry, d'ye think?”
“Oh! that's easy to guess,” said the Baron; “some yokel or other. But I'll cast her horoscope. Come here girl, and tell me on what day you were born?”
“I don't know, sir,” said the girl, “I was picked up just here after having been brought down by the river about fifteen years ago.”
Then the Baron knew who she was, and when they went away, he rode back and said to the girl: “Hark ye, girl, I will make your fortune. Take this letter to my brother in Scarborough, and you will be settled for life.” And the girl took the letter and said she would go. Now this was what he had written in the letter:
“Dear Brother,—Take the bearer and put her to death immediately.
“Yours affectionately,
“Albert.”
So soon after the girl set out for Scarborough, and slept for the night at a little inn. Now that very night a band of robbers broke into the inn, and searched the girl, who had no money, and only the letter. So they opened this and read it, and thought it a shame. The captain of the robbers took a pen and paper and wrote this letter:
“Dear Brother,—Take the bearer and marry her to my son immediately.
“Yours affectionately,
“Albert.”
And then he gave it to the girl, bidding her begone. So she went on to the Baron's brother at Scarborough, a noble knight, with whom the Baron's son was staying. When she gave the letter to his brother, he gave orders for the wedding to be prepared at once, and they were married that very day.
Soon after, the Baron himself came to his brother's castle, and what was his surprise to find that the very thing he had plotted against had come to pass. But he was not to be put off that way; and he took out the girl for a walk, as he said, along the cliffs. And when he got her all alone, he took her by the arms, and was going to throw her over. But she begged hard for her life. “I have not done anything,” she said: “if you will only spare me, I will do whatever you wish. I will never see you or your son again till you desire it.” Then the Baron took off his gold ring and threw it into the sea, saying: “Never let me see your face till you can show me that ring;” and he let her go.
The poor girl wandered on and on, till at last she came to a great noble's castle, and she asked to have some work given to her; and they made her the scullion girl of the castle, for she had been used to such work in the fisherman's hut.
Now one day, who should she see coming up to the noble's house but the Baron and his brother and his son, her husband. She didn't know what to do; but thought they would not see her in the castle kitchen. So she went back to her work with a sigh, and set to cleaning a huge big fish that was to be boiled for their dinner. And, as she was cleaning it, she saw something shine inside it, and what do you think she found? Why, there was the Baron's ring, the very one he had thrown over the cliff at Scarborough. She was right glad to see it, you may be sure. Then she cooked the fish as nicely as she could, and served it up.
Well, when the fish came on the table, the guests liked it so well that they asked the noble who cooked it. He said he didn't know, but called to his servants: “Ho, there, send up the cook that cooked that fine fish.” So they went down to the kitchen and told the girl she was wanted in the hall. Then she washed and tidied herself and put the Baron's gold ring on her thumb and went up into the hall.
When the banqueters saw such a young and beautiful cook they were surprised. But the Baron was in a tower of a temper, and started up as if he would do her some violence. So the girl went up to him with her hand before her with the ring on it; and she put it down before him on the table. Then at last the Baron saw that no one could fight against Fate, and he handed her to a seat and announced to all the company that this was his son's true wife; and he took her and his son home to his castle; and they all lived as happy as could be ever afterwards.""",
    # FOURTH STORY: the three heads of the well
    """Long before Arthur and the Knights of the Round Table, there reigned in the eastern part of England a king who kept his Court at Colchester. 
In the midst of all his glory, his queen died, leaving behind her an only daughter, about fifteen years of age, who for her beauty and kindness was the wonder of all that knew her. But the king hearing of a lady who had likewise an only daughter, had a mind to marry her for the sake of her riches, though she was old, ugly, hook-nosed, and hump-backed. Her daughter was a yellow dowdy, full of envy and ill-nature; and, in short, was much of the same mould as her mother. But in a few weeks the king, attended by the nobility and gentry, brought his deformed bride to the palace, where the marriage rites were performed. They had not been long in the Court before they set the king against his own beautiful daughter by false reports. The young princess having lost her father's love, grew weary of the Court, and one day, meeting with her father in the garden, she begged him, with tears in her eyes, to let her go and seek her fortune; to which the king consented, and ordered her mother-in-law to give her what she pleased. She went to the queen, who gave her a canvas bag of brown bread and hard cheese, with a bottle of beer; though this was but a pitiful dowry for a king's daughter. She took it, with thanks, and proceeded on her journey, passing through groves, woods, and valleys, till at length she saw an old man sitting on a stone at the mouth of a cave, who said: “Good morrow, fair maiden, whither away so fast?”
“Aged father,” says she, “I am going to seek my fortune.”
“What have you got in your bag and bottle?”
“In my bag I have got bread and cheese, and in my bottle good small beer. Would you like to have some?”
“Yes,” said he, “with all my heart.”
With that the lady pulled out her provisions, and bade him eat and welcome. He did so, and gave her many thanks, and said: “There is a thick thorny hedge before you, which you cannot get through, but take this wand in your hand, strike it three times, and say, 'Pray, hedge, let me come through,' and it will open immediately; then, a little further, you will find a well; sit down on the brink of it, and there will come up three golden heads, which will speak; and whatever they require, that do.” Promising she would, she took her leave of him. Coming to the hedge and using the old man's wand, it divided, and let her through; then, coming to the well, she had no sooner sat down than a golden head came up singing:
“Wash me, and comb me,
And lay me down softly.
And lay me on a bank to dry,
That I may look pretty,
When somebody passes by.”
“Yes,” said she, and taking it in her lap combed it with a silver comb, and then placed it upon a primrose bank. Then up came a second and a third head, saying the same as the former. So she did the same for them, and then, pulling out her provisions, sat down to eat her dinner.
Then said the heads one to another: “What shall we weird for this damsel who has used us so kindly?”
The first said: “I weird her to be so beautiful that she shall charm the most powerful prince in the world.”
The second said: “I weird her such a sweet voice as shall far exceed the nightingale.”
The third said: “My gift shall be none of the least, as she is a king's daughter, I'll weird her so fortunate that she shall become queen to the greatest prince that reigns.”
She then let them down into the well again, and so went on her journey. She had not travelled long before she saw a king hunting in the park with his nobles. She would have avoided him, but the king, having caught a sight of her, approached, and what with her beauty and sweet voice, fell desperately in love with her, and soon induced her to marry him.
This king finding that she was the King of Colchester's daughter, ordered some chariots to be got ready, that he might pay the king, his father-in-law, a visit. The chariot in which the king and queen rode was adorned with rich gems of gold. The king, her father, was at first astonished that his daughter had been so fortunate, till the young king let him know of all that had happened. Great was the joy at Court amongst all, with the exception of the queen and her club-footed daughter, who were ready to burst with envy. The rejoicings, with feasting and dancing, continued many days. Then at length they returned home with the dowry her father gave her.
The hump-backed princess, perceiving that her sister had been so lucky in seeking her fortune, wanted to do the same; so she told her mother, and all preparations were made, and she was furnished with rich dresses, and with sugar, almonds, and sweetmeats, in great quantities, and a large bottle of Malaga sack. With these she went the same road as her sister; and coming near the cave, the old man said: “Young woman, whither so fast?”
“What's that to you?” said she.
“Then,” said he, “what have you in your bag and bottle?”
She answered: “Good things, which you shall not be troubled with.”
“Won't you give me some?” said he.
“No, not a bit, nor a drop, unless it would choke you.”
The old man frowned, saying: “Evil fortune attend ye!”
Going on, she came to the hedge, through which she espied a gap, and thought to pass through it; but the hedge closed, and the, thorns ran into her flesh, so that it was with great difficulty that she got through. Being now all over blood, she searched for water to wash herself, and, looking round, she saw the well. She sat down on the brink of it, and one of the heads came up, saying: “Wash me, comb me, and lay me down softly,” as before, but she banged it with her bottle, saying, “Take that for your washing.” So the second and third heads came up, and met with no better treatment than the first. Whereupon the heads consulted among themselves what evils to plague her with for such usage.
The first said: “Let her be struck with leprosy in her face.”
The second: “Let her voice be as harsh as a corn-crake's.”
The third said: “Let her have for husband but a poor country cobbler.”
Well, she goes on till she came to a town, and it being market-day, the people looked at her, and, seeing such a mangy face, and hearing such a squeaky voice, all fled but a poor country cobbler. Now he not long before had mended the shoes of an old hermit, who, having no money gave him a box of ointment for the cure of the leprosy, and a bottle of spirits for a harsh voice. So the cobbler having a mind to do an act of charity, was induced to go up to her and ask her who she was.
“I am,” said she, “the King of Colchester's daughter-in-law.”
“Well,” said the cobbler, “if I restore you to your natural complexion, and make a sound cure both in face and voice, will you in reward take me for a husband?”
“Yes, friend,” replied she, “with all my heart!”
With this the cobbler applied the remedies, and they made her well in a few weeks; after which they were married, and so set forward for the Court at Colchester. When the queen found that her daughter had married nothing but a poor cobbler, she hanged herself in wrath. The death of the queen so pleased the king, who was glad to get rid of her so soon, that he gave the cobbler a hundred pounds to quit the Court with his lady, and take to a remote part of the kingdom, where he lived many years mending shoes, his wife spinning the thread for him.""",
    # FIFTH STORY: mr. vinegar
    """Mr. and Mrs. Vinegar lived in a vinegar bottle. 
Now, one day, when Mr. Vinegar was from home, Mrs. Vinegar, who was a very good housewife, was busily sweeping her house, when an unlucky thump of the broom brought the whole house clitter-clatter, clitter-clatter, about her ears. In an agony of grief she rushed forth to meet her husband.
On seeing him she exclaimed, “Oh, Mr. Vinegar, Mr. Vinegar, we are ruined, I have knocked the house down, and it is all to pieces!” Mr. Vinegar then said: “My dear, let us see what can be done. Here is the door; I will take it on my back, and we will go forth to seek our fortune.”
They walked all that day, and at nightfall entered a thick forest. They were both very, very tired, and Mr. Vinegar said: “My love, I will climb up into a tree, drag up the door, and you shall follow.” He accordingly did so, and they both stretched their weary limbs on the door, and fell fast asleep.
In the middle of the night Mr. Vinegar was disturbed by the sound of voices underneath, and to his horror and dismay found that it was a band of thieves met to divide their booty.
“Here, Jack,” said one, “here's five pounds for you; here, Bill, here's ten pounds for you; here, Bob, here's three pounds for you.”
Mr. Vinegar could listen no longer; his terror was so great that he trembled and trembled, and shook down the door on their heads. Away scampered the thieves, but Mr. Vinegar dared not quit his retreat till broad daylight.
He then scrambled out of the tree, and went to lift up the door. What did he see but a number of golden guineas. “Come down, Mrs. Vinegar,” he cried; “come down, I say; our fortune's made, our fortune's made! Come down, I say.”
Mrs. Vinegar got down as fast as she could, and when she saw the money she jumped for joy. “Now, my dear,” said she, “I'll tell you what you shall do. There is a fair at the neighbouring town; you shall take these forty guineas and buy a cow. I can make butter and cheese, which you shall sell at market, and we shall then be able to live very comfortably.”
Mr. Vinegar joyfully agrees, takes the money, and off he goes to the fair. When he arrived, he walked up and down, and at length saw a beautiful red cow. It was an excellent milker, and perfect in every way. “Oh,” thought Mr. Vinegar, “if I had but that cow, I should be the happiest, man alive.”
So he offers the forty guineas for the cow, and the owner said that, as he was a friend, he'd oblige him. So the bargain was made, and he got the cow and he drove it backwards and forwards to show it.
By-and-by he saw a man playing the bagpipes—Tweedle-dum tweedle-dee. The children followed him about, and he appeared to be pocketing money on all sides. “Well,” thought Mr. Vinegar, “if I had but that beautiful instrument I should be the happiest man alive—my fortune would be made.”
So he went up to the man. “Friend,” says he, “what a beautiful instrument that is, and what a deal of money you must make.” “Why, yes,” said the man, “I make a great deal of money, to be sure, and it is a wonderful instrument.” “Oh!” cried Mr. Vinegar, “how I should like to possess it!” “Well,” said the man, “as you are a friend, I don't much mind parting with it; you shall have it for that red cow.” “Done!” said the delighted Mr. Vinegar. So the beautiful red cow was given for the bagpipes.
He walked up and down with his purchase; but it was in vain he tried to play a tune, and instead of pocketing pence, the boys followed him hooting, laughing, and pelting.
Poor Mr. Vinegar, his fingers grew very cold, and, just as he was leaving the town, he met a man with a fine thick pair of gloves. “Oh, my fingers are so very cold,” said Mr. Vinegar to himself. “Now if I had but those beautiful gloves I should be the happiest man alive.” He went up to the man, and said to him, “Friend, you seem to have a capital pair of gloves there.” “Yes, truly,” cried the man; “and my hands are as warm as possible this cold November day.” “Well,” said Mr. Vinegar, “I should like to have them.”. “What will you give?” said the man; “as you are a friend, I don't much mind letting you have them for those bagpipes.” “Done!” cried Mr. Vinegar. He put on the gloves, and felt perfectly happy as he trudged homewards.
At last he grew very tired, when he saw a man coming towards him with a good stout stick in his hand.
“Oh,” said Mr. Vinegar, “that I had but that stick! I should then be the happiest man alive.” He said to the man: “Friend! what a rare good stick you have got.” “Yes,” said the man; “I have used it for many a long mile, and a good friend it has been; but if you have a fancy for it, as you are a friend, I don't mind giving it to you for that pair of gloves.” Mr. Vinegar's hands were so warm, and his legs so tired, that he gladly made the exchange.
As he drew near to the wood where he had left his wife, he heard a parrot on a tree calling out his name: “Mr. Vinegar, you foolish man, you blockhead, you simpleton; you went to the fair, and laid out all your money in buying a cow. Not content with that, you changed it for bagpipes, on which you could not play, and which were not worth one-tenth of the money. You fool, you—you had no sooner got the bagpipes than you changed them for the gloves, which were not worth one-quarter of the money; and when you had got the gloves, you changed them for a poor miserable stick; and now for your forty guineas, cow, bagpipes, and gloves, you have nothing to show but that poor miserable stick, which you might have cut in any hedge.” On this the bird laughed and laughed, and Mr. Vinegar, falling into a violent rage, threw the stick at its head. The stick lodged in the tree, and he returned to his wife without money, cow, bagpipes, gloves, or stick, and she instantly gave him such a sound cudgelling that she almost broke every bone in his skin.
""",
]

# initialize lists to store sentiment scores for each sentence
positive_scores = []
neutral_scores = []
negative_scores = []

# process each story one by one
for index, story in enumerate(stories, start=1):
    sentences = sent_tokenize(story)
    csv_output = []

    # analyze the sentiment of each sentence
    for i, sentence in enumerate(sentences, 1):
        # get sentiment labels and confidences for the sentence
        sentiment_labels, confidences = get_sentiment(sentence)
        highest_label_index = confidences.index(max(confidences))

        # append the result in the format shown below
        csv_output.append(
            [
                i,
                sentence,
                sentiment_labels[highest_label_index],
                confidences[2],
                confidences[1],
                confidences[0],
            ]
        )

        # append sentiment scores for the sentence to respective lists
        positive_scores.append(confidences[2])
        neutral_scores.append(confidences[1])
        negative_scores.append(confidences[0])

    # define the output CSV file name for the current story in the "data" directory
    csv_file = os.path.join("../data/original", f"story_{index}_sentiment_data.csv")

    # save the data to a CSV file in the "data" directory
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)  # create a CSV writer object to write data
        writer.writerow(
            [
                "Number",
                "Sentence",
                "Highest_Label",
                "Positive_Score",
                "Neutral_Score",
                "Negative_Score",
            ]
        )  # header row
        writer.writerows(csv_output)  # write all other rows

    # print a success message
    print(f"Story {index} has been processed and saved to {csv_file}.")
