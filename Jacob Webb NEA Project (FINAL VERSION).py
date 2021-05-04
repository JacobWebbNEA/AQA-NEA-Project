#Essentials 
import pygame 
import sys, os
from pygame.locals import *
import time
import threading
import numpy as np
import json


pygame.init() #initalises Pygame 
clock = pygame.time.Clock() #Pygames inbuilt clock

#Window Attributes
pygame.display.set_caption("NEA PROJECT - JACOB  WEBB") #Name
SCREEN_SIZE = (1280, 720) #Constant of the screen size 
Screen = pygame.display.set_mode(SCREEN_SIZE,0,32) #Screen attributes 

#initialise Sound 

pygame.mixer.pre_init(44100, -16, 2, 512) #pre-initalises the mixer module

#RGB Values for colours - CONSTANTS
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
TRANSPARENT = (0,0,0,0)
WHITE = (255, 255, 254)


#Player Class
class Player:
    def __init__(self):
        self._PlayerSprite = pygame.image.load("Sprites\PFront.png")
        self._PlayerSprite = pygame.transform.scale(self._PlayerSprite,(45,45))
        self._JumpCount = 2
        self._Left = False
        self._Right = False
        self._PlayerY = 0
        self._PlayerSpriteLeft = pygame.image.load("Sprites\PLeft.png")
        self._PlayerSpriteLeft = pygame.transform.scale(self._PlayerSpriteLeft,(40,40))
        self._PlayerSpriteRight = pygame.image.load("Sprites\PRight.png")
        self._PlayerSpriteRight = pygame.transform.scale(self._PlayerSpriteRight,(40,40))
        self._PlayerRect = pygame.Rect(100, 200, self._PlayerSprite.get_width(),self._PlayerSprite.get_height())
        self._JumpTime = 0
        self._JumpCount = 0
        self._PlayerScore = 0
        self._PlayerLives = 3


    #Getters for returning the private attributes to the main program 

    def GetPlayerSprite(self):
        return self._PlayerSprite

    def GetPlayerSpriteLeft(self):
        return self._PlayerSpriteLeft

    def GetPlayerSpriteRight(self):
        return self._PlayerSpriteRight 

    def GetJumpCount(self):
        return self._JumpCount

    def GetLeft(self):
        return self._Left

    def GetRight(self):
        return self._Right

    def GetPlayerY(self):
        return self._PlayerY

    def GetPlayerRect(self):
        return self._PlayerRect
        
    def GetPlayerRectX(self):
        return self._PlayerRect[0]

    def GetPlayerRectY(self):
        return self._PlayerRect[1]

    def GetJumpTime(self):
        return self._JumpTime

    def GetJumpCount(self):
        return self._JumpCount

    def GetPlayerScore(self):
        return self._PlayerScore

    def GetPlayerLives(self):
        return self._PlayerLives
        
    #Code to update private attributes when needed
    
    def UpdatePlayerScore(self,n):
        self._PlayerScore += n
        return self._PlayerScore

    def UpdatePlayerY(self):
        self._PlayerY += 4

        if self._PlayerY > 8:
            self._PlayerY = 8

    def UpdatePlayerRect(self,n):
        self._PlayerRect += n


    def UpdateJumpAndAirTime(self,Collisions):
        if Collisions["Bottom"]:
            self._PlayerY = 0
            self._JumpTime = 0
            self._JumpCount = 2
        else:
            self._JumpTime += 1

    def UpdateJumpCount(self,n):
        self._JumpCount -= n

    def UpdatePlayerLives(self):
        self._PlayerLives -= 1

    def UpdatePlayerRectX(self, n):
        self._PlayerRect[0] += n

    def UpdatePlayerRectY(self, n):
        self._PlayerRect[1] += n

    def PlayerDeathPenalty(self):
        self._PlayerScore -= 15

    def ResetPlayerPos(self):
        self._PlayerRect[0] = 200
        self._PlayerRect[1] = 0

    def SetRightFalse(self):
        self._Right = False

    def SetLeftFalse(self):
        self._Left = False

    def SetRightTrue(self):
        self._Right = True

    def SetLeftTrue(self):
        self._Left = True

    def UpdateJumpHeight(self,n):
        self._PlayerY -= n

    def LoadFileScore(self,LoadedData):
        self._PlayerScore = LoadedData[0]

    def UpdatePlayerRectLeft(self, Tile):
        self._PlayerRect.left = Tile.right
        

    def UpdatePlayerRectRight(self, Tile):
        self._PlayerRect.right = Tile.left
        

    def UpdatePlayerRectTop(self,Tile):
        self._PlayerRect.top = Tile.bottom
        

    def UpdatePlayerRectBottom(self,Tile):
        self._PlayerRect.bottom = Tile.top



   


#Sound Loading

def GetCurrentMusicState():
    LevelOneMusicLoaded = False #Boolean Value that checks whether the music for Level One Is Loaded
    MenuMusicLoaded = False #Boolean Value that checks whether the music for The menu Is Loaded
    return LevelOneMusicLoaded,MenuMusicLoaded

def LoadSoundEffects():
    #Loads the various Sound effects present in the game
    OptionSelectSound = pygame.mixer.Sound("SFX\OptionClicked.ogg")
    JumpSound = pygame.mixer.Sound("SFX\JumpSoundEffect.wav")
    CollectSound = pygame.mixer.Sound("SFX\CollectSound.wav")
    ItemUsed = pygame.mixer.Sound("SFX\ItemUsed.ogg")
    ItemFailure = pygame.mixer.Sound("SFX\ItemFailure.ogg")
    return OptionSelectSound,JumpSound,CollectSound,ItemUsed,ItemFailure

#Background and stage assets loading


def LevelOneImageAssets():
    #Loads all of the Assets in level One Map
    LevelOne = pygame.image.load("Tiles\Cave.jpg")
    Underground = pygame.image.load("Tiles\\Underground Tile.png")
    CaveDirt = pygame.image.load("Tiles\CaveDirt.png")
    CaveLeftLedge = pygame.image.load("Tiles\Cave Dirt Left Edge.png")
    CaveRightLedge = pygame.image.load("Tiles\Cave Dirt Right Edge.png")
    CaveFloor = pygame.image.load("Tiles\Cave Floor.png")
    CaveRoof = pygame.image.load("Tiles\Cave Roof.png")
    CaveWallLeft = pygame.image.load("Tiles\Cave Wall left.png")
    CaveWallRight = pygame.image.load("Tiles\Cave Wall Right.png")
    CaveDoubleSider = pygame.image.load("Tiles\Cave Double Sider.png")
    CaveWallTopLeft = pygame.image.load("Tiles\Cave Wall Top Left.png")
    CaveWallTopRight = pygame.image.load("Tiles\Cave Wall Top Right.png")
    return LevelOne, Underground,CaveDirt,CaveLeftLedge,CaveRightLedge,CaveFloor,CaveRoof,CaveWallLeft,CaveWallRight,CaveDoubleSider,CaveWallTopLeft,CaveWallTopRight


def LevelTwoImages():
    #Loads all of the Assets that would be in Level Two 
    Grass = pygame.image.load("Grass Tile.png")
    Dirt = pygame.image.load("Dirt Tile.png")
    return Grass, Dirt


def CollectablesAssetSetup():
    #Loads all data that is needed for collectables in the game 
    GiantCoin = pygame.image.load("Sprites\Gold Coin.png")  
    CoinCollected = False   #Boolean value checks if the coin has been collected 
    GiantCoinRect = GiantCoin.get_rect()  #Gets the rect (essentially hitbox) of the Coin 
    Diamond = pygame.image.load("Sprites\Diamond.png")
    DiamondCollected = False #Boolean value checks if the Diamond has been collected 
    DiamondRect = Diamond.get_rect() #Gets the rect (essentially hitbox) of the Diamond
    Gemstone = pygame.image.load("Sprites\Green Gem.png")
    GemCollected = False #Boolean value checks if the Gem has been collected
    GemstoneRect = Gemstone.get_rect() #Gets the rect (essentially hitbox) of the Gem
    return GiantCoin,CoinCollected,GiantCoinRect,Diamond,DiamondCollected,DiamondRect,Gemstone,GemCollected,GemstoneRect 


#Finish Condition
def LoadFinishConditionAssets():
    GoldenBrief = pygame.image.load("Sprites\Golden Briefcase.png")
    GoldenBriefRect = GoldenBrief.get_rect() #gets the rect of the briefcase
    return GoldenBrief,GoldenBriefRect #returns both variables 


#TestMap (dev map)


def LoadMapOne():
    OpenMap = open("LevelOne.json")  #Opens a pre-existing JSON file stored in the location of the py file
    LevelOneMap = json.load(OpenMap) #The variable LevelOneMap is assigned to the contents of the JSON file 
    return LevelOneMap #Variable LevelOneMap is returned 

def TilesCollision(Tiles): #Takes the parameter of Tiles - whatever is passed as the argument 
    Collides = [] #New Empty list is created 
    for Tile in Tiles: 
        if ThePlayer.GetPlayerRect().colliderect(Tile): #Checks that for each tile does the player collide 
            Collides.append(Tile) #if so the tile collided with is added to the Collide List 
    return Collides #returns collides to main program 

def Move(Movement, Tiles): #Takes two parameters - whatever is passed as these arguments
    CollisionType = {"Top": False, "Bottom": False, "Right": False, "Left": False} #Dictionary assigned to Boolean values
    ThePlayer.UpdatePlayerRectX(Movement[0]) #Uses a public Method for the Player class to update the x position of the player 
    Collides = TilesCollision(Tiles) #runs the TilesCollision function and Collides is assigned to the return of this 
    for Tile in Collides: #Checks each Tile in the collides list 
        if Movement[0] > 0: #If a collision is made the value will always be above 0
            ThePlayer.UpdatePlayerRectRight(Tile) #The Player Class.right is updated to the Tile.Left
            CollisionType["Right"] = True #the Dictionary assigned to CollisonType Right is set to True
                                
        elif Movement[0] < 0: #If a collision is made the value will always be above 0
            ThePlayer.UpdatePlayerRectLeft(Tile) #The Player Class.left is updated to the Tile.Right
            CollisionType["Left"] = True #the Dictionary assigned to CollisonType Left is set to True

    ThePlayer.UpdatePlayerRectY(Movement[1]) #Uses a public Method for the Player class to update the Y position of the player
    
    Collides = TilesCollision(Tiles) #runs the TilesCollision function and Collides is assigned to the return of this
    
    for Tile in Collides:  #Checks each Tile in the collides list
        if Movement[1] > 0: #If a collision is made the value will always be above 0
            ThePlayer.UpdatePlayerRectBottom(Tile) #The Player Class.Bottom is updated to the Tile.Top
            CollisionType['Bottom'] = True #the Dictionary assigned to CollisonType Bottom is set to True
                                
        elif Movement[1] < 0: #If a collision is made the value will always be above 0
            ThePlayer.UpdatePlayerRectTop(Tile) #The Player Class.Top is updated to the Tile.Bottom
            CollisionType["Top"] = True #the Dictionary assigned to CollisonType Top is set to True
    return CollisionType 




def MouseProperties(): #Function for getting Mouse values 
    MouseX, MouseY = pygame.mouse.get_pos() #Gets X and Y position of Mouse 
    MouseLocation = [MouseX, MouseY] #Gets Combined co-ordinates 
    Clicked = False #Boolean value to check if cliked 
    return MouseX, MouseY,MouseLocation,Clicked #returns above variables to main program 



def LevelSelectionProperties():
    #Boolean Logic for checking if a Level has been Selected
    Selection = False
    LevelSelected = False
    return Selection,LevelSelected


def SetLevelLocked():
    #Sets Logic for checking whether the Levels are Locked or Unlocked 
    IsLevelTwoLocked = True
    IsLevelThreeLocked = True
    IsLevelFourLocked = True
    return IsLevelTwoLocked,IsLevelThreeLocked,IsLevelFourLocked


def SetLevelActiveValues():
    #Sets Logic for checking whether any of the Levels are Active 
    LevelOneActive = False
    LevelTwoActive = False
    LevelThreeActive = False
    LevelFourActive = False

    #Logic for checking whether the levels have been reset or have been cleared 
    LevelOneCleared = False
    LevelOneReset = False
    MenuChoice = "Default" 
    return LevelOneActive,LevelTwoActive,LevelThreeActive,LevelFourActive,LevelOneCleared,LevelOneReset,MenuChoice




#Main Menu and GUI Images

def SetOptionsMenuValue():
    #Logic to check whether in Options Menu
    InOptionsMenu = False
    return InOptionsMenu

def SetLevelMenuValue():
    #Logic to check whether in Level Menu
    InLevelMenu = False
    return InLevelMenu

def LoadMenuAssetts():
    #Loads all the images associciated with the Menu
    
    MainMenu = pygame.image.load("GUI\Main Menu.png")
    LevelSelectMenu = pygame.image.load("GUI\Level Select.png")
    PlayButton = pygame.image.load("GUI\Play Button.png")
    OptionsButton = pygame.image.load("GUI\Options Button.png")
    ExitButton = pygame.image.load("GUI\Exit Button.png")
    LevelOneIcon = pygame.image.load("GUI\Caves.png")
    LevelOneComplete = pygame.image.load("GUI\Caves Completed.png")
    LevelTwoIconLocked = pygame.image.load("GUI\Daybreak Locked.png")
    LevelTwoUnlocked = pygame.image.load("GUI\Daybreak.png")
    LevelThreeIconLocked = pygame.image.load("GUI\Secluded Forest Locked.png")
    LevelThreeUnlocked = pygame.image.load("GUI\Secluded Forest.png")
    LevelFourIconLocked = pygame.image.load("GUI\Rush Hour Locked.png")
    LevelFourUnlocked = pygame.image.load("GUI\Rush Hour.png")
    EndGameButton = pygame.image.load("GUI\End Game Button.png")
    LoadGameButton = pygame.image.load("GUI\Load Game Button.png")
    SaveGameButton = pygame.image.load("GUI\Save Game Button.png")
    return MainMenu,LevelSelectMenu,PlayButton,OptionsButton,ExitButton,LevelOneIcon,LevelOneComplete,LevelTwoIconLocked,LevelTwoUnlocked,LevelThreeIconLocked,LevelThreeUnlocked,LevelFourIconLocked,LevelFourUnlocked,EndGameButton,LoadGameButton,SaveGameButton





def CreateButtonRects():
    #Creates the Hitboxes of the buttons and moves them to their apprpiate co-ordinates on the screen
    ButtonRect = PlayButton.get_rect()
    LeveIconRect = LevelOneIcon.get_rect()
    PlayButtonPos = ButtonRect.move(410,175)
    OptionsButtonPos = ButtonRect.move(410,345)
    ExitButtonsPos = ButtonRect.move(410, 495)
    LoadGamePos = ButtonRect.move(35,580)
    SaveGamePos = ButtonRect.move(480,580)
    LevelOneIconPos = LeveIconRect.move(20,255)
    EndGamePos = ButtonRect.move(910,580)

    return ButtonRect,LeveIconRect,PlayButtonPos,OptionsButtonPos,ExitButtonsPos,LoadGamePos,SaveGamePos,LevelOneIconPos,EndGamePos



def MainMenuDisplay():
    if InMainMenu == True: #If The MainMenu Logic is True

        #Display The Following to the Screen
        Screen.blit(MainMenu,[0,0])
        Screen.blit(PlayButton,[410, 175])
        Screen.blit(OptionsButton,[410, 345])
        Screen.blit(ExitButton,[410,495])


def UserChoice(MenuChoice):
    #if MenuChoice is PLAY then it will take to level select menu
    if MenuChoice == "PLAY":
        LevelSelect()
        #This may be defunct code, a menu re-work was introduced that made this function somewhat obsolete 
        

def LoadOptionsMenuAssets():
    #Loads all the images associated with the Options Menu
    
    OptionsMenu = pygame.image.load("GUI\Options Menu.png")
    MusicOnButton = pygame.image.load("GUI\Music On Button.png")
    MusicOffButton = pygame.image.load("GUI\Music Off Button.png")
    SoundFXOnButton = pygame.image.load("GUI\SoundFX on Button.png")
    SoundFXOffButton = pygame.image.load("GUI\SoundFX off Button.png")
    BackButton = pygame.image.load("GUI\Back Button.png")
    return OptionsMenu, MusicOnButton, MusicOffButton,SoundFXOnButton,SoundFXOffButton,BackButton


def SetOptionMenuRects():
    #Creates the Hitboxes for the Option Menu buttons and and moves them to their apprpiate co-ordinates on the screen
    BackButtonPos = ButtonRect.move(10,580)
    OptionsButtonRect = SoundFXOnButton.get_rect()
    MusicButtonPos = OptionsButtonRect.move(15,285)
    SoundButtonPos = OptionsButtonRect.move(660,285)
    return BackButtonPos,OptionsButtonRect,MusicButtonPos,SoundButtonPos

    

def OptionsMenuScreen():
    #Logic and Display for Options Menu Screen
    
    if InOptionsMenu == True: 
        Screen.blit(OptionsMenu,[0,0]) #Displays The GUI image for OptionsMenu
        if MusicOn == True:
            Screen.blit(MusicOnButton,[15,285]) #The GUI Button Image for Music On will be displayed at Co-ords

        if MusicOn != True:
            Screen.blit(MusicOffButton,[15,285]) #The GUI Button Image for Music Off will be displayed at Co-ords

        if SoundFXOn == True:
            Screen.blit(SoundFXOnButton,[660,285]) #The GUI Button Image for SoundFX on will be displayed at Co-ords

        if SoundFXOn != True:
            Screen.blit(SoundFXOffButton,[660,285]) #The GUI Button Image for SoundFX Off will be displayed at Co-ords

        Screen.blit(BackButton,[10,580]) #Back Button GUI is displayed at Co-ords
    
        

def LevelSelect():
    if InLevelMenu == True:
        #Displays the GUI images for the Level Menu at the Co-ords assigned to them 
        Screen.blit(LevelSelectMenu,[0,0]) 
        Screen.blit(LevelOneIcon,[20,255])
        Screen.blit(EndGameButton,[910,580])
        Screen.blit(LoadGameButton,[35,580])
        Screen.blit(SaveGameButton,[480,580])
        

        if LevelOneCleared == True:
            Screen.blit(LevelOneComplete,[20,255]) #Displays the GUI image for LevelOneComplete to the Screen,replacing the previous image
        
        if IsLevelTwoLocked:
            Screen.blit(LevelTwoIconLocked,[315,255]) #Displays the GUI image for a Locked Level Two 
        else:
            Screen.blit(LevelTwoUnlocked,[315,255]) #Displays the GUI image for Unlocked Level Two to the Screen,replacing Locked Image 
        if IsLevelThreeLocked:
            Screen.blit(LevelThreeIconLocked,[620,255]) #Displays the GUI image for a Locked Level Three

        else:
            Screen.blit(LevelThreeUnlocked,[620,255]) #Displays the GUI image for Unlocked Level Three to the Screen, replacing Locked Image

        if IsLevelFourLocked:
            Screen.blit(LevelFourIconLocked,[955,255]) #Displays the GUI image for a Locked Level Four

        else:
            Screen.blit(LevelFourUnlocked,[955,255]) #Displays the GUI image for Unlocked Level Four to the Screen, replacing Locked Image

        if LevelSelected == True:
            #Logic checks if a level has been selected an returns the values of the levels (would add more returns if was doing other levels)
            return LevelOneActive 
        
    

#Class for the Stack that Manages items 
class ItemStack():
    def __init__(self):
        self.ItemsList = list() #Creates a attribute that is a list 
        self.MaxSize = 4 #creates an attribute which is 4
        self.Top = 0 #creates an attribute set to 0 (the Top, keeps track of the top of the stack)

    def Push(self, Item): 
        if self.Top >= self.MaxSize: #Logic to check if the value of The Top is bigger than the maximum allowed size 
            return ("Item Stack Full") #will return the message that the stack is full

        self.ItemsList.append(Item) #will add the item to the Stack
        self.Top += 1 #The Value of the Stack will increment 
        return ("Added") #Visual checker to verify that the item has been added 

    def Pop(self):
        if self.Top <= 0: #checks if the value of top is below or equal to 0
            return ("No Items!") #it will return the message to the main program 

        global ItemBeingUsed #Value of Variable ItemBeingUsed will be Globally updated 

        ItemBeingUsed = self.ItemsList.pop() #it will remove the item at the top of the stack
        self.Top -= 1 #Top decrements by 1 as item has been removed 
        return ItemBeingUsed + str(" Is active ") #Returns the name of the item and indicates to the player that is active 

    def Peek(self):
        try:
            return self.ItemsList[self.Top-1] #it will attempt to peek at the list position 1 below the value of top
        except:
            "Attempted to peek an empty stack" #Generally if the code above did not have anything in it, it would thrown an error, so an except statement prevents this
            return




#CAMERA
def SetCameraPos():
    #Sets Camera Co-ords 
    Camera = [0,0]
    return Camera


#ITEM

def ItemImageAsset():
    #Loads all the images associated with items 
    ItemGUI = pygame.image.load("GUI\Item GUI.png")
    JumpBoots = pygame.image.load("GUI\Jump Boots.png")
    Overclock = pygame.image.load("GUI\Overclock.png")
    Speedboost = pygame.image.load("GUI\Speedboost.png")
    return ItemGUI,JumpBoots,Overclock,Speedboost



def GetItemRects():
    #Gets the Hitboxes of the items 
    JumpBootsRect = JumpBoots.get_rect()
    SpeedboostRect = Speedboost.get_rect()
    return JumpBootsRect,SpeedboostRect



def SetCollectedState():
    #Logic for checking if the items have been collected 
    JumpBootsCollected = False
    SpeedboostCollected = False
    return JumpBootsCollected, SpeedboostCollected


def SetItemBeingUsed():
    #Variable with string is set - will be updated when items are picked up
    ItemBeingUsed = "none"
    return ItemBeingUsed


 
def SetItemActiveState():
    #Logic values for checking if the items are active 
    SpeedboostActive = False
    ShieldActive = False
    OverclockActive = False
    JumpBootsActive = False
    return SpeedboostActive,ShieldActive,OverclockActive,JumpBootsActive


def ItemPlacement(JumpBootsCollected, SpeedboostCollected):
            #Item placement
            if JumpBootsCollected == False:
                Screen.blit(JumpBoots,[6460 - Camera[0],1350 - Camera[1]]) #displays the image of JumpBoots to the co-ordinates 
                JumpBootsPos = JumpBootsRect.move(12239 - Camera[0],2139 - Camera[1]) #Moves the hitbox of the Jumpboots to associated position of image
                
                if ThePlayer.GetPlayerRect().colliderect(JumpBootsPos): #if the Player Hitbox collides with the hitbox for the JumpBoots
                    ThePlayer.UpdatePlayerScore(5) #Player Score is updated by 5 using public method
                    CollectSound.play() #Collect SFX 
                    print("worked") #visual checker to check it worked 
                    print(ItemsPickedUp.Push("Jump Boots")) #Jump Boots are added to the stack
                    JumpBootsCollected = True #Logic for JumpBoots updated 

            if SpeedboostCollected == False:
                Screen.blit(Speedboost,[3750 - Camera[0],1100 - Camera[1]]) #displays the image of SpeedBoost to the co-ordinates
                SpeedboostPos = SpeedboostRect.move(6780 - Camera[0],1800 - Camera[1]) #Moves the hitbox of the Speedboost to associated position of image
                
                if ThePlayer.GetPlayerRect().colliderect(SpeedboostPos): #if the Player Hitbox collides with the hitbox for the Speedboost
                    ThePlayer.UpdatePlayerScore(5) #Player Score is updated by 5 using public method
                    CollectSound.play() #Collect SFX 
                    print("worked") #visual checker to check it worked 
                    print(ItemsPickedUp.Push("Speedboost")) #Speedboost is added to the stack
                    SpeedboostCollected = True #Logic for Speedboost updated 

            if JumpBootsCollected == True:
                if JumpBootsActive == False and ItemsPickedUp.Peek() == "Jump Boots": #Checks if when peeked the item is Jump Boots 
                    Screen.blit(JumpBoots,[1060,30]) #if it is found to be JumpBoots the image for Jump Boots is displayed in the held Item slot

            if SpeedboostCollected == True:
                if JumpBootsActive == False and ItemsPickedUp.Peek() == "Speedboost": #Checks if when peeked the item is Speedboost
                    Screen.blit(Speedboost,[1065,20]) #if it is found to be speedboost the image for Jump Boots is displayed in the held Item slot
            return JumpBootsCollected, SpeedboostCollected

def GetItemState(JumpBootsActive,SpeedboostActive,OverclockActive,ShieldActive):
    #depending on what item is active, all other items are set to false, this means no one item can be active at the same time as another 
    if JumpBootsActive == True:
            SpeedboostActive = False
            ShieldActive = False
            OverclockActive = False

    if SpeedboostActive == True:
        JumpBootsActive = False
        ShieldActive = False
        OverclockActive = False



    if ItemBeingUsed == "Speedboost":
        SpeedboostActive = True
        JumpBootsActive = False
        ShieldActive = False
        OverclockActive = False

    if ItemBeingUsed == "Shield":
        ShieldActive = True
        SpeedboostActive = False
        JumpBootsActive = False
        OverclockActive = False

    if ItemBeingUsed == "Overclock":
        OverclockActive = True
        SpeedboostActive = False
        JumpBootsActive = False
        ShieldActive = False

    if ItemBeingUsed == "Jump Boots":
        JumpBootsActive = True
        SpeedboostActive = False
        ShieldActive = False
        OverclockActive = False

    return JumpBootsActive,SpeedboostActive,OverclockActive,ShieldActive



def LevelFinishAndCollectables(LevelOneCleared,CoinCollected,DiamondCollected,GemCollected): #Parameters passed from whatever arguments from main program 
    if LevelOneCleared == False:
        Screen.blit(GoldenBrief,[8260 - Camera[0],1400 - Camera[1]]) #Displays The golden briefcase at the co-ordinates given (end of map)
        GoldenBriefPos = GoldenBriefRect.move(15825 - Camera[0],2170 - Camera[1]) #Moves the hitbox of the briefcase to the associated position of the image 
        if ThePlayer.GetPlayerRect().colliderect(GoldenBriefPos):  #if the Player hitbox collides with the Briefcase hitbox
            CollectSound.play() #Play Collect Sound
            LevelOneCleared = True  #Level will be classed as cleared
    
    if CoinCollected == False:
        Screen.blit(GiantCoin,[85 - Camera[0],875 - Camera[1]]) #Displays The Giant Coin at the co-ordinates given
        GiantCoinPos = GiantCoinRect.move((-400) - Camera[0],1600 - Camera[1]) #Moves the hitbox of the Giant Coin to the associated position of the image
        if ThePlayer.GetPlayerRect().colliderect(GiantCoinPos): #if the Player hitbox collides with the Giant Coin hitbox
            CollectSound.play() #CollectSFX
            ThePlayer.UpdatePlayerScore(10) #Player Score is updated by 10 using a public method
            CoinCollected = True #Will remove the coin from displaying

    if DiamondCollected == False:
        Screen.blit(Diamond,[7125 - Camera[0],230 - Camera[1]]) #Displays The Diamond at the co-ordinates given
        DiamondPos = DiamondRect.move(13626 - Camera[0],337 - Camera[1]) #Moves the hitbox of the Diamond to the associated position of the image
        if  ThePlayer.GetPlayerRect().colliderect(DiamondPos): #if the Player hitbox collides with the Diamond hitbox
            CollectSound.play() #CollectSFX
            ThePlayer.UpdatePlayerScore(10) #Player Score is updated by 10 using a public method
            DiamondCollected = True #Will remove the Diamond from displaying

    if GemCollected == False:
        Screen.blit(Gemstone,[5400 - Camera[0],1050 - Camera[1]]) #Displays The Gem at the co-ordinates given
        GemPos = GemstoneRect.move(10175 - Camera[0],1800 - Camera[1]) #Moves the hitbox of the gem to the associated position of the image
        if ThePlayer.GetPlayerRect().colliderect(GemPos): #if the Player hitbox collides with the gem hitbox
            CollectSound.play() #CollectSFX
            ThePlayer.UpdatePlayerScore(10) #Player Score is updated by 10 using a public method
            GemCollected = True #Will remove the gem from displaying

    return LevelOneCleared,CoinCollected,DiamondCollected,GemCollected


def GetCameraPos():
    #Allows the Camera position to change based on the player position 
    Camera[0] += (ThePlayer.GetPlayerRect().x - Camera[0]-680)/ 10 #Parallax effect
    Camera[1] += (ThePlayer.GetPlayerRect().y - Camera[1] -360)/ 10 #Parallax effect


def CameraLock(Camera):
    #will lock the camera in place if the player Y position goes above or below 
    if Camera[1] <= -1:
        Camera[1] = 0

    if Camera[1] >= 750:
        Camera[1] = 750

    return Camera

def DisplayThePlayerScore():
    #Renders the string of the Players Score and displays it at co-ords
    DisplayPlayerScore = PlayerScoreFont.render("Score: " +str(ThePlayer.GetPlayerScore()),True,WHITE)
    Screen.blit(DisplayPlayerScore,[10, 10])

def TrackMovement():
    TrackPlayerMovement = [0, 0] #List for default co-ords 
    if ThePlayer.GetLeft() == True and SpeedboostActive == False:
        TrackPlayerMovement[0] -= 7 #Will move the Player 7 frames to the Left
        Screen.blit(ThePlayer.GetPlayerSpriteLeft(), (ThePlayer.GetPlayerRect().x-Camera[0],(ThePlayer.GetPlayerRect().y+5)-Camera[1])) #Blit the Left spacing sprite, take away 5 from position to account for sprite size difference

    if ThePlayer.GetLeft() == True and SpeedboostActive == True:
        TrackPlayerMovement[0] -= 10.5 #Will Move the Player 10.5 Frames to the left (Higher Number to give illusion of higher speed)
        Screen.blit(ThePlayer.GetPlayerSpriteLeft(),(ThePlayer.GetPlayerRect().x-Camera[0],(ThePlayer.GetPlayerRect().y+5)-Camera[1]))
        

    if ThePlayer.GetRight() == True and SpeedboostActive == False:
        TrackPlayerMovement[0] += 7 #Will move the Player 7 frames to the Right
        Screen.blit(ThePlayer.GetPlayerSpriteRight(), (ThePlayer.GetPlayerRect().x-Camera[0],(ThePlayer.GetPlayerRect().y+5)-Camera[1])) #Blit the Right spacing sprite, take away 5 from position to account for sprite size difference

    if ThePlayer.GetRight() == True and SpeedboostActive == True:
        TrackPlayerMovement[0] += 10.5 #Will Move the Player 10.5 Frames to the Right (Higher Number to give illusion of higher speed)
        Screen.blit(ThePlayer.GetPlayerSpriteRight(), (ThePlayer.GetPlayerRect().x-Camera[0],(ThePlayer.GetPlayerRect().y+5)-Camera[1]))
            
    if ThePlayer.GetRight() != True and ThePlayer.GetLeft() != True:
        Screen.blit(ThePlayer.GetPlayerSprite(), (ThePlayer.GetPlayerRect().x-Camera[0],ThePlayer.GetPlayerRect().y-Camera[1])) #Displays the forward facing sprite at correct position
        

    TrackPlayerMovement[1] += ThePlayer.GetPlayerY() #The Y co-ordinate for tracking the PlayerMovement will be updated adding the value returned from the method call
    ThePlayer.UpdatePlayerY() #Public method for updating the Y co-ords of the Player class is called 
    return TrackPlayerMovement

#Timer function, deals with rendering and displaying font

def SetTimerValues():
    ElapsedTime = 0.00 #Time values
    ElapsedTimeRounded = ElapsedTime
    TimerFont = pygame.font.SysFont("Pixellari",30) #Font creation
    DisplayTimerFont = "" #logic for displaying 
    return ElapsedTime,ElapsedTimeRounded, TimerFont,DisplayTimerFont

def Timer():
    global ElapsedTime,ElapsedTimeRounded #updates preceding variables globally
    while TimerEnded == False: #thread condition
        ElapsedTime = pygame.time.get_ticks() / 1000.0 - StartTime #will get the exact time in milliseconds since get_ticks () is ran
        ElapsedTimeRounded = round(ElapsedTime,2) #rounds for better presentation
        print(ElapsedTimeRounded)

StartTime = 0.00 #sets the time before the level is clicked, can be taken away from overall ticks to get time since for just level

def GetTicksBeforeLevelStart():
    global StartTime
    while LevelClicked == False:
        StartTime = pygame.time.get_ticks() / 1000.0 #will get the exact time in milliseconds since get_ticks () is ran
        print(StartTime)
        
    
         
#ActualTime = ElapsedTimeRounded

def LoadMenuMusic(MenuMusicLoaded):
    #Loads The Music and logic for the Main Menu
    if MenuMusicLoaded == False:
        pygame.mixer.music.unload() #unloads previous music in mixer
        pygame.mixer.music.load("Music\Wacky Worker Theme.mp3")
        pygame.mixer.music.play(-1) #LOOP
        MenuMusicLoaded = True
    return MenuMusicLoaded
        


def LoadLevelOneMusic(LevelOneMusicLoaded):
    #Loads The Music and logic for the First Level
    if LevelOneMusicLoaded == False:
        pygame.mixer.music.unload() #unloads previous music in mixer
        pygame.mixer.music.load("Music\8BitCave.mp3")
        pygame.mixer.music.play(-1) #LOOP
        LevelOneMusicLoaded = True
    return LevelOneMusicLoaded





#GameOver Variables 

def SetGameOverState():
    #logic for GameOver check
    GameOver = False
    return GameOver

def SetPlayerName():
    #Player Name is set as an empty string and the PlayerScore is gathered as a string through the use of a public method, logic that checks if the player name has been got is put in place 
    PlayerName = ""
    PlayerScoreAsString = str(ThePlayer.GetPlayerScore())
    GotPlayerName = False
    return PlayerName,PlayerScoreAsString,GotPlayerName


def GameOverScreenAssets():
    #Logic and Assets for the Gameover screen are set up)
    GetPlayerNameScreen = pygame.image.load("GUI\EnterNameScreen.png")
    GetPlayerFont = pygame.font.SysFont("LLPixel",109)
    InGetPlayerNameMenu = True
    HS_Screen = pygame.image.load("GUI\HS_Screen.png")
    return GetPlayerNameScreen,GetPlayerFont,InGetPlayerNameMenu,HS_Screen

def SetHSMusicState():
    #Logic for Highscore music
    HighscoreMusicLoaded = False
    return HighscoreMusicLoaded


def SetSortedState():
    #Logic for checking if a sort has been performed 
    Sorted = False
    return Sorted



def LoadHighScoreMusic(HighscoreMusicLoaded):
    #Loads The Music and logic for the Highscores
    if HighscoreMusicLoaded == False:
        pygame.mixer.music.unload() #unloads previous music in mixer
        pygame.mixer.music.load("Music\Highscores Music.mp3")
        pygame.mixer.music.play(-1)#LOOP
        HighscoreMusicLoaded = True
    return HighscoreMusicLoaded
        


def OpenHSFile():
    HighscoreList = open("highscores.txt","r") #Opens in Read mode
    for line in HighscoreList:
        ReadHighscores = HighscoreList.read()
        ScoresSplit = ReadHighscores.splitlines()
        ScoresSplit = ReadHighscores.split(",") #Splits each individual Users Stats via the comma (Score/Name)
    HighscoreList.close() #closes the file

    return ScoresSplit


def ScoreAndSort(ScoresSplit):
    ScoresList = [int(each.split("-")[1]) for each in ScoresSplit] # Splits the List into Purely Scores as integers, ready for Merge sort
    NameList = [str(each.split("-")[0]) for each in ScoresSplit] # Splits the List into Purely Names as a string

    NameList.append(PlayerName)
    ScoresList.append(ThePlayer.GetPlayerScore())
    ScoresListUnsorted = np.array(ScoresList,dtype=object) #Creates an array that can be composed of different data types (in this case int)
    NameListUnsorted = np.array(NameList,dtype=object) #Creates an array that can be composed of different data types (in this case string)
    print(ScoresListUnsorted)
    print(NameListUnsorted)
    print(NameList)

    NamesAndScoresCombined = np.column_stack((ScoresListUnsorted,NameListUnsorted)) #Creates a 2D array from the existing lists where one index is an integer data type and one is a String data type 
    print(NamesAndScoresCombined)
    

    print("Unsorted:" ,ScoresList)


    MergeSort(NamesAndScoresCombined) #Sorts the List into Ascending Order
    print(NamesAndScoresCombined)

    NamesAndScoresCombinedRev = np.flip(NamesAndScoresCombined) #Takes the Ascending order 2D array and makes it descending 
    print(NamesAndScoresCombinedRev) #Prints Descending order

    return NamesAndScoresCombinedRev



#Recursive Merge Sort Algorithm

def MergeSort(ListToSort): #Move Position of Names as well
    if len(ListToSort)> 1:
        MiddleOfList = len(ListToSort)// 2
        LeftIndex = ListToSort[:MiddleOfList]
        RightIndex = ListToSort[MiddleOfList:]

        if isinstance(ListToSort,np.ndarray): # Ensures data is not lost during merge sort - Reference How these lines were found on the internet 
            LeftIndex = LeftIndex.copy()
            RightIndex = RightIndex.copy()
            
            

        MergeSort(LeftIndex) #recursively calls itself for the value in LeftIndex
        MergeSort(RightIndex) #recursively calls itself for the Value in RightIndex 

        LeftCounter = 0
        RightCounter =0
        CurrentCounter =0
        
        while LeftCounter < len(LeftIndex) and RightCounter < len(RightIndex): #while the length of LeftIndex array is smaller than the value of LeftCounter and the length of the RightIndex is smaller than the value of RightCounter
            if LeftIndex[LeftCounter][0] <= RightIndex[RightCounter][0]: #will then check if the First array in the 2D array of LeftIndex dicated by the value of LeftCounter is smaller or equal to the First array in the 2D array of RightIndex dictated by the value of the RightCounter
                ListToSort[CurrentCounter]=LeftIndex[LeftCounter] #if this is true then the position of ListToSort at the value of CurrentCounter will be set to equal the position of the LeftIndex at the value of the LeftCounter 
                LeftCounter += 1 #LeftCounter will then increment by 1 
            else:
                ListToSort[CurrentCounter]=RightIndex[RightCounter]
                RightCounter += 1 # RightCounter increments by 1 inside nested loop
            CurrentCounter += 1 #CurrentCounter Increments by 1 outside of nested loop

        while LeftCounter < len(LeftIndex):
            ListToSort[CurrentCounter]=LeftIndex[LeftCounter]
            LeftCounter += 1 #LeftCounter increments by 1
            CurrentCounter += 1 #Current Counter increments by 1

        while RightCounter < len(RightIndex): #while the value of RightCounter is smaller than the len of the array Right Index, the proceeding code is ran 
            ListToSort[CurrentCounter]=RightIndex[RightCounter] #The position in the sorted list, dictated by the value of the CurrentCounter is set to equal the position in the RightIndex, dictated by the value of RightCounter
            RightCounter += 1 #RightCounter increments by 1
            CurrentCounter += 1 #CurrentCounter increments by 1


def GetTopFiveScores(NamesAndScoresCombinedRev):
    #Creates a string made up of the Players Name and Their Score for the Top 5 Scores 
    HighScoreOne = str(NamesAndScoresCombinedRev[0][0])+"-"+str(NamesAndScoresCombinedRev[0][1]) 
    HighScoreTwo = str(NamesAndScoresCombinedRev[1][0])+"-"+str(NamesAndScoresCombinedRev[1][1])
    HighScoreThree = str(NamesAndScoresCombinedRev[2][0])+"-"+str(NamesAndScoresCombinedRev[2][1])
    HighScoreFour = str(NamesAndScoresCombinedRev[3][0])+"-"+str(NamesAndScoresCombinedRev[3][1])
    HighScoreFive = str(NamesAndScoresCombinedRev[4][0])+"-"+str(NamesAndScoresCombinedRev[4][1])

    return HighScoreOne,HighScoreTwo,HighScoreThree,HighScoreFour,HighScoreFive






def DisplayHighscores(Screen,PlayerScoreAsString,HighScoreOne,HighScoreTwo,HighScoreThree,HighScoreFour,HighScoreFive):
    Screen.blit(HS_Screen,[0,0]) #Displays the GUI image for the highscores at the co-ords given 
    HighscoreFont = pygame.font.SysFont("Pixellari", 60) #creates the highscore font
    YourFont = pygame.font.SysFont("Pixellari", 80) #creates the Playerscore font

    DisplayYourScore = YourFont.render(str(ThePlayer.GetPlayerScore()), True, WHITE) #Players font

    Screen.blit(DisplayYourScore,(678,175)) #displays the players score at given co-ords 
    
    #Renders all of the HighScore strings
    DisplayHSFontOne = HighscoreFont.render(HighScoreOne, True, WHITE)
    DisplayHSFontTwo = HighscoreFont.render(HighScoreTwo, True, WHITE)
    DisplayHSFontThree = HighscoreFont.render(HighScoreThree, True, WHITE)
    DisplayHSFontFour = HighscoreFont.render(HighScoreFour , True, WHITE)
    DisplayHSFontFive = HighscoreFont.render(HighScoreFive, True, WHITE)

    #Displays all of the Highscore strings 
    Screen.blit(DisplayHSFontOne,(450,325))
    Screen.blit(DisplayHSFontTwo, (450,395))
    Screen.blit(DisplayHSFontThree, (450,470))
    Screen.blit(DisplayHSFontFour, (450,545))
    Screen.blit(DisplayHSFontFive, (450,615))
    


def SaveNewScores():
    HighscoreList = open("highscores.txt","w") #Opens a pre-existing file of highscores
    HighscoreList.write("\n") #New line wrote 
    HighscoreList.write(HighScoreOne) #writes highscore one 
    HighscoreList.write(",") #proceeded by a comma
    HighscoreList.write(HighScoreTwo)#proceeded by highscoretwo
    HighscoreList.write(",") #proceeded by a comma
    HighscoreList.write(HighScoreThree) #proceesed by highscore three
    HighscoreList.write(",") #proceesed by a comma
    HighscoreList.write(HighScoreFour) #proceeded by highscore four
    HighscoreList.write(",")  #proceeded by a comma
    HighscoreList.write(HighScoreFive) #proceeded by highscore five
    HighscoreList.close() #closes the file


def GetPlayerName():
    #Displays the Player name screen, renders the players name and display it at given co-ords 
    Screen.blit(GetPlayerNameScreen,[0,0])
    DisplayPlayerFont = GetPlayerFont.render(PlayerName,True,WHITE)
    Screen.blit(DisplayPlayerFont,[768,220])
    


#PLAYER LIFE STATE


def PlayerLivesAssets():
    #Loads all the assets for the PlayerLives
    ThreeLives = pygame.image.load("Sprites\ThreeLives.png")
    TwoLives = pygame.image.load("Sprites\TwoLives.png")
    OneLife = pygame.image.load("Sprites\OneLife.png")
    LifeLostSFX = pygame.mixer.Sound("Music\LifeLost.wav")
    return ThreeLives,TwoLives,OneLife,LifeLostSFX


def LivesLostScreenAssets():
    #Loads all assets for game over screen
    GameOverScreen = pygame.image.load("GUI\GameOver Screen.png")
    GameOverButton = pygame.image.load("GUI\GameOver Button.png")
    return GameOverScreen,GameOverButton

    
def SetLivesLostButton():
    #creates the hitbox for the gameover button and moves it to corresponding position of image
    GameOverButtonRect = GameOverButton.get_rect()
    GameOverButtonPos = GameOverButtonRect.move(355,490)
    return GameOverButtonRect,GameOverButtonPos

def SetLostLivesState():
    #logic for lives
    LostAllLives = False
    return LostAllLives


def SetLostLivesMusicState():
    #logic for music in gameover
    LostAllLivesMusicLoaded = False
    return LostAllLivesMusicLoaded



def LostAllLivesMusic():
    #Logic for playing music when all lives are lost
    global LostAllLivesMusicLoaded
    if LostAllLivesMusicLoaded == False:
        pygame.mixer.music.unload() #unloads previous music
        LostAllLivesMusic = pygame.mixer.music.load("Music\OutOfLivesMusic.mp3") #loads game over music 
        pygame.mixer.music.play(-1) #Loops
        LostAllLivesMusicLoaded = True


def OutOfLives():
    global LostAllLives
    LostAllLivesMusic() #calls LostAllLivesFunction
    LostAllLives = True #updates logic


    #Displays GUI Screen and button to the display at given co-ords  
    Screen.blit(GameOverScreen,[0,0])
    Screen.blit(GameOverButton,[355,490])
    
    
    

def GetLifeState():
    #Logic for ensuring correct image is displayed based on lives
    if ThePlayer.GetPlayerLives() == 3: #Gets the value of Playerlives through a public method and checks if it is 3
        Screen.blit(ThreeLives,[125,10]) #blits one heart 
    

    if ThePlayer.GetPlayerLives() == 2: #Gets the value of Playerlives through a public method and checks if it is 2
        Screen.blit(TwoLives,[125,10]) #blits two hearts 

    if ThePlayer.GetPlayerLives() == 1: #Gets the value of Playerlives through a public method and checks if it is 1
        Screen.blit(OneLife,[125,10])#blits image of one heart

    if ThePlayer.GetPlayerLives() == 0: #Gets the value of Playerlives through a public method and checks if it is 0
        OutOfLives() #Runs OutofLives function
        

def PlayerLoseLife(): 
    if ThePlayer.GetPlayerRectY() > 1600:
        #Checks if the PlayerPosition is offscreen indicating they have fallen off
        print("Player dead")
        ThePlayer.ResetPlayerPos() #calls public method to reset x and y position 
        ThePlayer.UpdatePlayerLives() #calls  public method to remove a life 
        ThePlayer.PlayerDeathPenalty() #calls public method to remove 15 from score 
        LifeLostSFX.play()  #Life Lost Sound effect


#FILE STUFF

def SetFileAndLoadMenuStates():
    #Logic for file Load Menu and Save Menu
    InLoadMenu = False
    InSaveMenu = False
    FileOneLoaded = False
    FileTwoLoaded = False
    return InLoadMenu,InSaveMenu,FileOneLoaded,FileTwoLoaded




def SetFileStates():
    #Logic for checking if the save files are empty 
    FileOneEmpty = True
    FileTwoEmpty = True
    return FileOneEmpty,FileTwoEmpty

def SaveFileAssets():
    #Loading all image assets for GUI of Save and Load 
    SavesMenuPart = pygame.image.load("GUI\FileSection.png")
    SaveFileWithData = pygame.image.load("GUI\Save File With Data.png")
    SaveFileEmpty = pygame.image.load("GUI\Save File Empty.png")
    SaveFileOverwrite = pygame.image.load("GUI\Save File Overwrite.png")
    return SavesMenuPart,SaveFileWithData,SaveFileEmpty,SaveFileOverwrite

def SetFileRects():
    #Creates hitboxes for each save file image and moves them to an appropiate co-ords on the screen
    SaveFileRect = SaveFileEmpty.get_rect()
    LoadFileOnePos = SaveFileRect.move(10,180)
    LoadFileTwoPos = SaveFileRect.move(650,180)
    SaveFileOnePos = SaveFileRect.move(10,180)
    SaveFileTwoPos = SaveFileRect.move(650,180)
    return LoadFileOnePos,LoadFileTwoPos,SaveFileOnePos,SaveFileTwoPos

def SetFileSaveArrays():
    #creates an array to hold values for save file one and two 
    DumpedData = []
    DumpedDataTwo = []
    return DumpedData,DumpedDataTwo 

def LoadFileGUI():
    #Logic that will display an empty or active file depending on if either file is empty or not when in load menu
    InLevelMenu = False
    Screen.blit(SavesMenuPart,[0,0])
    if FileOneEmpty == True:
        Screen.blit(SaveFileEmpty,[10,180])

    if FileOneEmpty != True:
        LoadFileOneData()
        Screen.blit(SaveFileWithData,[10,180])
       
        
    if FileTwoEmpty == True:
        Screen.blit(SaveFileEmpty,[650,180])
        

    if FileTwoEmpty != True:
        LoadFileTwoData()
        Screen.blit(SaveFileWithData,[650,180])

def SaveFileGUI():
    #Logic that will display an empty or active file depending on if either file is empty or not when in save menu
    InLevelMenu = False
    Screen.blit(SavesMenuPart,[0,0])
    if FileOneEmpty == True:
        Screen.blit(SaveFileEmpty,[10,180])

    if FileOneEmpty != True:
        Screen.blit(SaveFileOverwrite,[10,180])

    if FileTwoEmpty == True:
        Screen.blit(SaveFileEmpty,[650,180])
        

    if FileTwoEmpty != True:
        Screen.blit(SaveFileOverwrite,[650,180])



def SaveFileOneData():
    FileOneData = open("FileOne.json","w") #opens a pre-existing json file in write mode

    #Creates a temporary list where value of variables will be added
    VariablesToDump = [] 

    #Value of Variables are added
    VariablesToDump.append(ThePlayer.GetPlayerScore())
    VariablesToDump.append(True)#Value for InLevelMenu - will always be true 
    VariablesToDump.append(IsLevelTwoLocked)
    VariablesToDump.append(IsLevelThreeLocked)
    VariablesToDump.append(IsLevelFourLocked)
    VariablesToDump.append(LevelOneCleared)

    json.dump(VariablesToDump,FileOneData) #The List is then dumped into the json file 


def SaveFileTwoData():
    FileTwoData = open("FileTwo.json","w") #The json file is opened for save 2

    #Creates a temporary list where value of variables will be added
    VariablesToDump = []

    #Value of Variables are added
    VariablesToDump.append(ThePlayer.GetPlayerScore())
    VariablesToDump.append(True)#Value for InLevelMenu - will always be true 
    VariablesToDump.append(IsLevelTwoLocked)
    VariablesToDump.append(IsLevelThreeLocked)
    VariablesToDump.append(IsLevelFourLocked)
    VariablesToDump.append(LevelOneCleared)
    json.dump(VariablesToDump,FileTwoData) #The List is then dumped into the json file
    


def LoadFileOneData():
    global DumpedData
    FileOneData = open("FileOne.json") #the json file is opened 
    DumpedData = json.load(FileOneData) #The contents of the file is loaded and are assigned to the variable DumpedData
    

def LoadFileTwoData():
    global DumpedDataTwo
    FileTwoData = open("FileTwo.json") #the json file is opened for save 2
    DumpedDataTwo = json.load(FileTwoData) #The contents of the file is loaded and are assigned to the variable DumpedDataTwo
    



def AssignLoadedVariables():
    #When a file save is clicked the values stored in the array will overwrite that of the variables beneath
    global InLevelMenu,IsLevelTwoLocked,IsLevelThreeLocked,IsLevelFourLocked, LevelOneCleared
    ThePlayer.LoadFileScore(DumpedData) #updates player score through use of public method 
    InLevelMenu = DumpedData[1]
    IsLevelTwoLocked = DumpedData[2]
    IsLevelThreeLocked = DumpedData[3]
    IsLevelFourLocked = DumpedData[4]
    LevelOneCleared = DumpedData[5]

def AssignLoadedVariablesTwo():
    #When a file save is clicked the values stored in the array will overwrite that of the variables beneath
    global InLevelMenu,IsLevelTwoLocked,IsLevelThreeLocked,IsLevelFourLocked, LevelOneCleared
    ThePlayer.LoadFileScore(DumpedDataTwo) #updates player score through use of public method
    InLevelMenu = DumpedDataTwo[1]
    IsLevelTwoLocked = DumpedDataTwo[2]
    IsLevelThreeLocked = DumpedDataTwo[3]
    IsLevelFourLocked = DumpedDataTwo[4]
    LevelOneCleared = DumpedDataTwo[5]

def GetTileSize():
    TILE_SIZE = CaveDirt.get_height() #Gets the height of the tile (just basically so you can get tile dimensions for maps)
    return TILE_SIZE

def PlayerScoreFontAndDisplay():
    PlayerScoreFont = pygame.font.SysFont("Gameplay", 30)
    DisplayPlayerScore = PlayerScoreFont.render("Score: " +str(ThePlayer.GetPlayerScore()),True,WHITE) #renders the string of score and then the players score
    return PlayerScoreFont,DisplayPlayerScore


def InMainMenuState():
    #logic for checking in main menu
    InMainMenu = True
    return InMainMenu


def SetSoundFXState():
    #logic for checking if the SoundFX are on 
    SoundFXValue = 0
    SoundFXOn = True
    return SoundFXValue, SoundFXOn

def SetMusicState():
    #logic for checking if the Music is on
    MusicValue = 0
    MusicOn = True
    return MusicValue, MusicOn


def CheckMusicState():
    if MusicValue % 2 == 0: #If the value of MusicValue has a remainder of 0 
        MusicOn = True  #then music on will be true, this means everytime the number is 0 or even, music will be on 

    else:
        MusicOn = False  #otherwise the music will be off, odd number 
        
    return MusicOn

def CheckSoundFXState():
    if SoundFXValue % 2 == 0: #If the value of SoundFXValue has a remainder of 0 
        SoundFXOn = True #then soundfx on will be true, this means everytime the number is 0 or even, music will be on 

    else:
        SoundFXOn = False #otherwise the music will be off, odd number
        
    return SoundFXOn

def SetBonus():
    Bonus = 100 #Default value for the bonus for a level
    return Bonus

def CalculateScoreBonus(Bonus):
    CachedBonus = Bonus - int(ElapsedTime)
    if CachedBonus <= 0:
        CachedBonus = 0
        
    Bonus -= int(ElapsedTime)
    if Bonus <= 0:
        Bonus = 0
        
    ThePlayer.UpdatePlayerScore(Bonus)
    return CachedBonus

def LoadLevelCompleteAssets():
    LevelCompleteFont = pygame.font.SysFont("Gameplay", 80)
    CavesComplete = pygame.image.load("GUI\Caves Complete.png")
    ProgressButton = pygame.image.load("GUI\Progress Button.png")
    ShowLevelOneComplete = False
    return LevelCompleteFont, CavesComplete,ProgressButton,ShowLevelOneComplete

def CavesCompleteScreen():
    DisplayTimeBonus = LevelCompleteFont.render(str(CachedBonus),True,WHITE) #renders the string of the time Bonus
    DisplayPlayerScore = LevelCompleteFont.render(str(ThePlayer.GetPlayerScore()),True,WHITE) #renders the string of the time Bonus
    Screen.blit(CavesComplete,[0,0])
    Screen.blit(ProgressButton,[685,515])
    Screen.blit(DisplayTimeBonus,[1050,340])
    Screen.blit(DisplayPlayerScore,[1050,435])


def GetRectForProgressButton():
    ProgressButtonRect = ProgressButton.get_rect()
    ProgessButtonPos = ProgressButtonRect.move(685,515)
    return ProgressButtonRect,ProgessButtonPos


def SetLevelOneCompleteMusic():
    LevelOneCompleteMusicLoaded = False
    return LevelOneCompleteMusicLoaded


def LoadLevelCompleteMusic(LevelOneCompleteMusicLoaded):
    if LevelOneCompleteMusicLoaded == False:
        pygame.mixer.music.unload()
        pygame.mixer.music.load("Music\Level Cleared theme.mp3")
        pygame.mixer.music.play(-1)
        LevelOneCompleteMusicLoaded = True
    return LevelOneCompleteMusicLoaded
        
    
    
    
    

#Threading

TimerEnded = False #Value for stopping the level timer condition
TimerThread = threading.Thread(target = Timer, daemon=True) #The thread for the timer function, Daemon allows main program to be closed 
TimerThread.start() #Starts the thread 


LevelClicked = False
GetTicksBeforeClick = threading.Thread(target = GetTicksBeforeLevelStart, daemon=True) 
GetTicksBeforeClick.start()





ThePlayer = Player() #Instantiate Class



#LOADING ALL ASSETS AND BOOLEAN LOGIC
PlayerScoreFont,DisplayPlayerScore = PlayerScoreFontAndDisplay()
LevelOneMusicLoaded,MenuMusicLoaded = GetCurrentMusicState()
OptionSelectSound,JumpSound,CollectSound,ItemUsed,ItemFailure = LoadSoundEffects()
InOptionsMenu = SetOptionsMenuValue()
LevelOne, Underground,CaveDirt,CaveLeftLedge,CaveRightLedge,CaveFloor,CaveRoof,CaveWallLeft,CaveWallRight,CaveDoubleSider,CaveWallTopLeft,CaveWallTopRight = LevelOneImageAssets()
Grass,Dirt = LevelTwoImages()
TILE_SIZE = GetTileSize()
LevelOneMap = LoadMapOne()
GoldenBrief,GoldenBriefRect = LoadFinishConditionAssets()
MouseX,MouseY,MouseLocation,Clicked = MouseProperties()
Selection,LevelSelected = LevelSelectionProperties()
GiantCoin,CoinCollected,GiantCoinRect,Diamond,DiamondCollected,DiamondRect,Gemstone,GemCollected,GemstoneRect = CollectablesAssetSetup()
IsLevelTwoLocked,IsLevelThreeLocked,IsLevelFourLocked = SetLevelLocked()
LevelOneActive,LevelTwoActive,LevelThreeActive,LevelFourActive,LevelOneCleared,LevelOneReset,MenuChoice = SetLevelActiveValues()
InLevelMenu = SetLevelMenuValue()
MainMenu,LevelSelectMenu,PlayButton,OptionsButton,ExitButton,LevelOneIcon,LevelOneComplete,LevelTwoIconLocked,LevelTwoUnlocked,LevelThreeIconLocked,LevelThreeUnlocked,LevelFourIconLocked,LevelFourUnlocked,EndGameButton,LoadGameButton,SaveGameButton = LoadMenuAssetts()
ButtonRect,LeveIconRect,PlayButtonPos,OptionsButtonPos,ExitButtonsPos,LoadGamePos,SaveGamePos,LevelOneIconPos,EndGamePos = CreateButtonRects()
Camera = SetCameraPos()
ItemGUI,JumpBoots,Overclock,Speedboost = ItemImageAsset()
JumpBootsRect,SpeedboostRect = GetItemRects()
JumpBootsCollected, SpeedboostCollected = SetCollectedState()
ItemBeingUsed = SetItemBeingUsed()
SpeedboostActive,ShieldActive,OverclockActive,JumpBootsActive = SetItemActiveState()
ItemsPickedUp = ItemStack()
ElapsedTime,ElapsedTimeRounded,TimerFont,DisplayTimerFont = SetTimerValues()
GameOver = SetGameOverState()
PlayerName,PlayerScoreAsString,GotPlayerName = SetPlayerName()
GetPlayerNameScreen,GetPlayerFont,InGetPlayerNameMenu,HS_Screen = GameOverScreenAssets()
HighscoreMusicLoaded = SetHSMusicState()
Sorted = SetSortedState()
ThreeLives,TwoLives,OneLife,LifeLostSFX = PlayerLivesAssets()
GameOverScreen,GameOverButton = LivesLostScreenAssets()
GameOverButtonRect,GameOverButtonPos = SetLivesLostButton()
LostAllLives = SetLostLivesState()
OptionsMenu, MusicOnButton, MusicOffButton,SoundFXOnButton,SoundFXOffButton,BackButton =  LoadOptionsMenuAssets()
LostAllLivesMusicLoaded = SetLostLivesMusicState()
InLoadMenu,InSaveMenu,FileOneLoaded,FileTwoLoaded = SetFileAndLoadMenuStates()
FileOneEmpty,FileTwoEmpty = SetFileStates()
SavesMenuPart,SaveFileWithData,SaveFileEmpty,SaveFileOverwrite = SaveFileAssets()
LoadFileOnePos,LoadFileTwoPos,SaveFileOnePos,SaveFileTwoPos = SetFileRects()
DumpedData,DumpedDataTwo = SetFileSaveArrays()
InMainMenu = InMainMenuState()
BackButtonPos,OptionsButtonRect,MusicButtonPos,SoundButtonPos = SetOptionMenuRects()
SoundFXValue,SoundFXOn = SetSoundFXState()
MusicValue, MusicOn = SetMusicState()
Bonus = SetBonus()
LevelCompleteFont, CavesComplete,ProgressButton,ShowLevelOneComplete = LoadLevelCompleteAssets()
ProgressButtonRect,ProgessButtonPos = GetRectForProgressButton()
LevelOneCompleteMusicLoaded = SetLevelOneCompleteMusic()



def CheckMusicAndSoundState():
    #if Music is on then music is playing, if not true it does not, same for sound
    if MusicOn != True:
        pygame.mixer.music.pause()

    if MusicOn == True:
        pygame.mixer.music.unpause()

    if SoundFXOn != True:
        pygame.mixer.pause()

    if SoundFXOn == True:
        pygame.mixer.unpause()


Running = True
#GameLoop


while Running:
    CheckMusicAndSoundState()
    if not GameOver:
        MenuMusicLoaded = LoadMenuMusic(MenuMusicLoaded)
        MainMenuDisplay()
        LevelSelect()
        OptionsMenuScreen()
        SoundFXOn = CheckSoundFXState()
        MusicOn = CheckMusicState() 

        if InLoadMenu == True:
            LoadFileGUI()

        if InSaveMenu == True:
            SaveFileGUI()
        

        if LevelOneActive == True:
            InLevelMenu = False
            Screen.blit(LevelOne,[0,0])
            GetCameraPos()
            LevelOneMusicLoaded = LoadLevelOneMusic(LevelOneMusicLoaded)

            
        
            CollideTiles = []


            #MAP LOADS
            RowY = 0
            for Row in LevelOneMap:
                RowX = 0
                for Tile in Row:
                    if Tile == "1":
                        Screen.blit(CaveRoof,(RowX * TILE_SIZE-Camera[0], RowY * TILE_SIZE-Camera[1]))
                    if Tile == "2":
                        Screen.blit(CaveDirt,(RowX * TILE_SIZE-Camera[0], RowY * TILE_SIZE-Camera[1]))
                    if Tile == "3":
                        Screen.blit(Underground,(RowX * TILE_SIZE-Camera[0], RowY * TILE_SIZE-Camera[1]))

                    if Tile == "4":
                        Screen.blit(CaveFloor,(RowX * TILE_SIZE-Camera[0], RowY * TILE_SIZE-Camera[1]))
                    if Tile == "5":
                        Screen.blit(CaveLeftLedge,(RowX * TILE_SIZE-Camera[0], RowY * TILE_SIZE-Camera[1]))

                    if Tile == "6":
                        Screen.blit(CaveRightLedge,(RowX * TILE_SIZE-Camera[0], RowY * TILE_SIZE-Camera[1]))

                    if Tile == "7":
                        Screen.blit(CaveWallRight,(RowX * TILE_SIZE-Camera[0], RowY * TILE_SIZE-Camera[1]))

                    if Tile == "8":
                        Screen.blit(CaveWallLeft,(RowX * TILE_SIZE-Camera[0], RowY * TILE_SIZE-Camera[1]))

                    if Tile == "9":
                        Screen.blit(CaveDoubleSider,(RowX * TILE_SIZE-Camera[0], RowY * TILE_SIZE-Camera[1]))

                    if Tile == "&":
                        Screen.blit(CaveWallTopLeft,(RowX * TILE_SIZE-Camera[0], RowY * TILE_SIZE-Camera[1]))

                    if Tile == "%":
                        Screen.blit(CaveWallTopRight,(RowX * TILE_SIZE-Camera[0], RowY * TILE_SIZE-Camera[1]))

                    if Tile != "0":
                        CollideTiles.append(pygame.Rect(RowX * TILE_SIZE, RowY * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    RowX += 1
                RowY +=1

            Screen.blit(ItemGUI,[1050,10])
            JumpBootsCollected, SpeedboostCollected = ItemPlacement(JumpBootsCollected,SpeedboostCollected)
            JumpBootsActive,SpeedboostActive,OverclockActive,ShieldActive = GetItemState(JumpBootsActive,SpeedboostActive,OverclockActive,ShieldActive)
            LevelOneCleared,CoinCollected,DiamondCollected,GemCollected = LevelFinishAndCollectables(LevelOneCleared,CoinCollected,DiamondCollected,GemCollected)
            DisplayThePlayerScore()
            TrackPlayerMovement = TrackMovement()
            Collisions = Move(TrackPlayerMovement, CollideTiles)
            ThePlayer.UpdateJumpAndAirTime(Collisions)
            Camera = CameraLock(Camera)
            GetLifeState()
            PlayerLoseLife()
            DisplayTimerFont = TimerFont.render(str("Time: ")+str(ElapsedTimeRounded),True,WHITE) #renders the string of the time
            Screen.blit(DisplayTimerFont,[230,12])

            if LevelOneCleared == True:
                TimerEnded = True
                TimerThread.join()
                CachedBonus = CalculateScoreBonus(Bonus)
                IsLevelTwoLocked = False 
                LevelOneActive = False
                ShowLevelOneComplete = True
                LoadLevelCompleteMusic(LevelOneCompleteMusicLoaded)
                CavesCompleteScreen()
            
                

            if LostAllLives == True:
                TimerEnded = True
                TimerThread.join()
                

    if GameOver == True:
        InLevelMenu = False
        HighscoreMusicLoaded = LoadHighScoreMusic(HighscoreMusicLoaded)
        if GotPlayerName == False:
            GetPlayerName()
        if GotPlayerName == True:
            if Sorted == False:
                ScoresSplit = OpenHSFile()
                NamesAndScoresCombinedRev = ScoreAndSort(ScoresSplit)
                HighScoreOne,HighScoreTwo,HighScoreThree,HighScoreFour,HighScoreFive = GetTopFiveScores(NamesAndScoresCombinedRev)
                SaveNewScores()
                Sorted = True
            DisplayHighscores(Screen,PlayerScoreAsString,HighScoreOne,HighScoreTwo,HighScoreThree,HighScoreFour,HighScoreFive)
    


    for event in pygame.event.get(): #Checks for specific events, looped
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            Running = False
        if event.type == KEYDOWN:       #Checks to see if a key is pressed down
            if  event.key == K_RIGHT:
                ThePlayer.SetRightTrue()
                ThePlayer.SetLeftFalse()

            if event.key == K_LEFT:
                ThePlayer.SetLeftTrue()
                ThePlayer.SetRightFalse()

            if InGetPlayerNameMenu == True:
                if event.key == pygame.K_BACKSPACE:   #DELETING
                    PlayerName = PlayerName[:-1] #Takes One away from the array of PlayerName

                elif event.key == pygame.K_RETURN: #if Enter is pressed
                    GotPlayerName = True #Got PlayerName is set to true

                else:
                    if len(PlayerName) < 5: #if the PlayerName is less than 5
                        PlayerName += event.unicode #Allow the player to add to the name 

        

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                ThePlayer.SetRightFalse() #Right is set to false by a public method

            if event.key == K_LEFT:
                ThePlayer.SetLeftFalse() #Left Is Set to false by a public method

            if event.key == K_UP:
                if ThePlayer.GetJumpCount() > 0 and JumpBootsActive == True:
                    JumpSound.play() #SFX
                    ThePlayer.UpdateJumpCount(2) #players Jump Count is updated by public method
                    ThePlayer.UpdateJumpHeight(60) #players Jump height is updated by public method

                if ThePlayer.GetJumpCount() > 0:
                    JumpSound.play() #SFX
                    ThePlayer.UpdateJumpCount(1) #players Jump Count is updated by public method
                    ThePlayer.UpdateJumpHeight(30) #players Jump height is updated by public method

            if event.key == K_SPACE and LevelOneActive != False:
                ItemUsed.play() #SFX
                print(ItemsPickedUp.Pop()) #will print return of the stack class method
                

        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if event.button == 1:
                Clicked = True
                #print("clicked")


                #Various logic checking if the mouse collides with a hitbox for a button at the appropiate time
                if PlayButtonPos.collidepoint(mouse_pos) and InMainMenu == True:
                    OptionSelectSound.play()
                    #print("Test")
                    InMainMenu = False
                    InLevelMenu = True
                    Selection = True

                if OptionsButtonPos.collidepoint(mouse_pos) and InMainMenu == True:
                    OptionSelectSound.play()
                    InMainMenu = False
                    InOptionsMenu = True
                    Selection = True

                if ExitButtonsPos.collidepoint(mouse_pos) and InMainMenu == True:
                    OptionSelectSound.play()
                    pygame.quit()
                    sys.exit()

                if BackButtonPos.collidepoint(mouse_pos) and InOptionsMenu == True:
                    OptionSelectSound.play()
                    InMainMenu = True
                    InOptionsMenu = False

                if MusicButtonPos.collidepoint(mouse_pos) and InOptionsMenu == True:
                    OptionSelectSound.play()
                    MusicValue += 1

                if SoundButtonPos.collidepoint(mouse_pos) and InOptionsMenu == True:
                    OptionSelectSound.play()
                    SoundFXValue += 1
                    

            
                if LevelOneIconPos.collidepoint(mouse_pos) and LevelOneCleared == False and InLevelMenu == True:
                    OptionSelectSound.play()
                    LevelClicked = True
                    GetTicksBeforeClick.join()
                    LevelSelected = True
                    InLevelMenu = False
                    LevelOneActive = True
                    

                if EndGamePos.collidepoint(mouse_pos) and InLevelMenu == True:
                    OptionSelectSound.play()
                    print("Ended Game")
                    GameOver = True

                if LoadGamePos.collidepoint(mouse_pos) and InLevelMenu == True:
                    OptionSelectSound.play()
                    print("In File Load Menu")
                    if os.path.isfile("FileOne.json"): #checks if the file exists
                        FileOneEmpty = False #if the file does exist it is not empty 

                    if os.path.isfile("FileTwo.json"):
                        FileTwoEmpty = False #otherwise it is
                    
                    InLoadMenu = True
                    InLevelMenu = False

                if SaveGamePos.collidepoint(mouse_pos) and InLevelMenu == True:
                    OptionSelectSound.play()
                    print("In File Save Menu")
                    if os.path.isfile("FileOne.json"):
                        FileOneEmpty = False

                    if os.path.isfile("FileTwo.json"):
                        FileTwoEmpty = False
                    
                    InSaveMenu = True
                    InLevelMenu = False
                    

                if LoadFileOnePos.collidepoint(mouse_pos) and InLoadMenu == True:
                    if FileOneEmpty == False:
                        AssignLoadedVariables()
                        FileOneLoaded = True
                    InLoadMenu = False

                if LoadFileTwoPos.collidepoint(mouse_pos) and InLoadMenu == True:
                    if FileTwoEmpty == False:
                        AssignLoadedVariablesTwo()
                        FileTwoLoaded = True
                    InLoadMenu = False
                    

                if SaveFileOnePos.collidepoint(mouse_pos) and InSaveMenu == True:
                    SaveFileOneData()
                    InSaveMenu = False
                    InLevelMenu = True
                    

                if SaveFileTwoPos.collidepoint(mouse_pos) and InSaveMenu == True:
                    SaveFileTwoData()
                    InSaveMenu = False
                    InLevelMenu = True
                    
        
                if GameOverButtonPos.collidepoint(mouse_pos) and LostAllLives == True:
                    OptionSelectSound.play()
                    GameOver = True
                    InLevelMenu = False

                if ProgessButtonPos.collidepoint(mouse_pos) and ShowLevelOneComplete == True:
                    OptionSelectSound.play()
                    InLevelMenu = True
                    ShowLevelOneComplete = False
                    
                    

    
   

    pygame.display.update() #updates display 
    clock.tick(60) #60 FPS




