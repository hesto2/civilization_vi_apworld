# Civlization 6

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

In Civilization VI, the tech and civic trees are both shuffled. This presents some interesting ways to play the game in a non-standard way.

There are a few changes that the Archipelago mod introduces in order to make this playable/fun. These are detailed in the __FAQ__ section below.

## What is the goal of Civilization VI when randomized?
The goal of randomized Civlization VI remains the same. Pursue any victory type you have enabled in your game settings, the one you normally go for may or may not be feasible based on how things have been changed up!

## Which items can be in another player's world?
All technologies and civics can be found in another player's world.

## What does another world's item look like in Civilization VI?
Each item from another world is represented as a researchable tech/civic in your normal tech/civic trees.

## When the player receives an item, what happens?
A short period after receiving an item, you will get a notification indicating you have discovered the relevant tech/civic. You will also get the regular popup that details what the given item has unlocked for you.

## FAQs
- Do I need the DLC to play this?
  - Yes, you need both Rise & Fall and Gathering Storm. If there is enough interest then I can eventually add support for Archipellago runs that don't require both expansions.

- Does this work with Multiplayer?
  - It does not and, despite my best efforts, probably won't until there's a new way for external programs to be able to interact with the game.

- Does my mod that reskins Barbarians as various Pro Wrestlers work with this??
  - Only one way to find out! Any mods that modify techs/civics will most likely cause issues, though.

- "Help! I can't see any of the items (techs/civics) that have been sent to me!"
  - Both trees by default will show you the researchable Archipelago locations. To view the normal tree, you can click "Toggle Archipelago Tree" on the top left corner of the tree view.

- "Oh no! I received the Machinery tech and now instead of getting an Archer next turn, I have to wait an additional 10 turns to get a Crossbowman!"
  - Vanilla prevents you from building units of the same class from an earlier tech level after you have researched a later variant. For example, this could be problematic if someone unlocks Crossbowmen for you right out the gate since you won't be able to make Archers (which have a much lower production cost).

  - Solution: You can now go in to the tech tree, click "Toggle Archipelago Tree" to view your unlocked techs, and then can click any tech you have unlocked to toggle whether it is currently active or not. __NOTE__: This is an experimental feature and may yield some unexpected behaviors. Please DM `@Hesto2` on Discord if you run into any issues.

- "I switched to a government that has more slots than I have policy cards!"
  - The base game would prevent you from confirming any policy changes/government switches if you did not fill each slot. This is problematic if you receive a high level government early in the game. To combat this, requirements for having all policy slots filled have been removed. __NOTE__: This means that you won't get turn blocking notifications telling you to switch governments when you unlock a new one or when you unlock a better version of a policy you currently have equipped. You will still be able to change your policies/government any time you complete a civic.