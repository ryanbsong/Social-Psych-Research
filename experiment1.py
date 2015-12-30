"""
experiment1.py
script for mentalizing experiment
PsychoPy2
created by Ryan Song 8/1/2014
"""

from psychopy import visual, core, gui, event, monitors
import numpy as np
import random
import pyglet
import csv
import os

def initial_dialog():
    """presents intial dialog"""
    dlg = gui.Dlg(title='experiment')
    dlg.addField('Subject Number', initial='1')
    dlg.addField('First Run?', initial='Yes',
                 choices=['1','2','3','4','5','6','7','8','9','10','11','12'])
    dlg.show()
    if gui.OK:
        sn = int(dlg.data[0])
        runNum = int(dlg.data[1]) - 1
        return(sn, runNum)
    else:
        core.quit()

def make_screen():
    """Generates screen variables"""
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screens = display.get_screens()
    win_res = [screens[-1].width, screens[-1].height]
    exp_mon = monitors.Monitor('exp_mon')
    exp_mon.setSizePix(win_res)
    win = visual.Window(size=win_res, screen=len(screens)-1, allowGUI=True,
                        fullscr=False, monitor=exp_mon, units='height',
                        color=(-1, -1, -1))
    #win.setMouseVisible(False)
    return(win_res, win)

def start_datafile(sn):
    """creates datafile (after checking for old one)"""
    # determines file name
    if sn < 10:
        snstr = '0' + str(sn)
    else:
        snstr = str(sn)
    datafileName = "experiment_" + snstr + ".csv"
    currentDirectory = os.listdir("." + os.sep + "Data")
    for file in currentDirectory:
        if file == datafileName:
            warningDialog = gui.Dlg(title="Warning!")
            warningDialog.addText("A data file with this number already exists.")
            warningDialog.addField("Overwrite?", choices=["No", "Yes"])
            warningDialog.addField("If not, enter new subject number:",
                                   initial="0")
            warningDialog.show()
            if gui.OK:
                if warningDialog.data[0] == "No":
                    subjectNumber = int(warningDialog.data[1])
                    if subjectNumber < 10:
                        snstr = '0' + str(subjectNumber)
                    else:
                        sntstr = str(subjectNumber)
                    datafileName = "experiment_" + snstr + ".csv"
            else:
                core.quit()
    datafile = open("." + os.sep + "Data" + os.sep + datafileName,
                    "ab")
    datafile.write("subjectnum,runnum,trialnum,trialbegintime,trialduration,trialjitterduration,\
    response,responsetime,person,personnum, prefitem, prefnum\n")
    return(datafile, sn)

def randomizer(ppl, pref, sn):
    """randomize person and preference matches for each trial"""
    # set random seed by subject number for replicability
    random.seed(sn)
    
    array = []
    runs = []
    index = []
    jitter = []
    
    # create and randomize indices for people and preference items
    for x in range(len(pref)):
        runs.append([])
        array.append([])
        index.append([])
        jitter.append([])
    initial = 0
    for list in array:
        counter = initial
        for x in range(len(pref)):
            if counter < len(pref)-1:
                counter += 1
                list.append(counter)
            else:
                counter = 0
                list.append(counter)
        initial += 1
    array *= len(ppl)/len(pref)
    random.shuffle(array)
    for x in range(len(pref)):
        for y in range(len(ppl)):
            index[x].append([y, array[y][x]])
        random.shuffle(index[x])
        
    # randomize people and preference items
    for x in range(len(index)):
        for y in range(len(index[x])):
            runs[x].append([ppl[index[x][y][0]], pref[index[x][y][1]]])
    return (runs, index)

def main():
    
    #run initial dialog
    [sn, runNum] = initial_dialog()
    
    #generate datafile
    [datafile, sn] = start_datafile(sn)
    writer = csv.writer(datafile)
    
    #create window
    [win_res, win] = make_screen()
    yScr = 1.
    xScr = float(win_res[0])/win_res[1]
    fontH = yScr/30
    wrapW = xScr/1.75
    
    #set constants
    textCol = [.2,.2,.2]
    timePerTrial = 5.0
    makeUpPerTrial = 0.0
    
    #import instructions
    instr = []
    inname = '.' + os.sep + 'Text' + os.sep + 'instructions.txt'
    infile = open(inname, 'r')
    for line in infile:
        instr.append(line.rstrip())
    instr.append("end")
    infile.close()
    
    # import preference items and create stimuli
    prefname = '.' + os.sep + 'Text' + os.sep + 'preferences.csv'
    preffile = open(prefname, 'rb')
    prefreader = csv.reader(preffile)
    prefstim = []
    for row in prefreader:
        prefstim.append(visual.TextStim(win, pos=[0, 0], text=row[0],
                                    height=fontH, color = textCol,
                                    wrapWidth=wrapW))
    preffile.close()
    
    # import people names and create stimuli
    pplname = '.' + os.sep + 'Text' + os.sep + 'people.csv'
    pplfile = open(pplname, 'rb')
    pplreader = csv.reader(pplfile)
    pplstim = []
    for row in pplreader:
        pplstim.append(visual.TextStim(win, pos=[0,yScr/8], text=row[0],
                                    height=fontH, color=textCol,
                                    wrapWidth=wrapW))
    pplfile.close()
    
    #randomize people and preferences for each run
    [runs, index] = randomizer(pplstim, prefstim, sn)
    
    #create fixation stimulus
    fix = visual.TextStim(win, pos=[0,0], text='+',height=fontH, color=textCol)
    
    #create 1 to 5 scale
    ratings = []
    scale = []
    ratings.append(visual.TextStim(win, pos=[-xScr/3.5,-yScr/8], text='Strongly Disagree',height=fontH, color=textCol))
    ratings.append(visual.TextStim(win, pos=[-xScr/7,-yScr/8], text='Disagree',height=fontH, color=textCol))
    ratings.append(visual.TextStim(win, pos=[0,-yScr/8], text='Neutral',height=fontH, color=textCol))
    ratings.append(visual.TextStim(win, pos=[xScr/7,-yScr/8], text='Agree',height=fontH, color=textCol))
    ratings.append(visual.TextStim(win, pos=[xScr/3.5,-yScr/8], text='Strongly Agree',height=fontH,color=textCol))
    
    scale.append(visual.TextStim(win, pos=[-xScr/3.5,-yScr/6], text='1',height=fontH, color=textCol))
    scale.append(visual.TextStim(win, pos=[-xScr/7,-yScr/6], text='2',height=fontH, color=textCol))
    scale.append(visual.TextStim(win, pos=[0,-yScr/6], text='3',height=fontH, color=textCol))
    scale.append(visual.TextStim(win, pos=[xScr/7,-yScr/6], text='4',height=fontH, color=textCol))
    scale.append(visual.TextStim(win, pos=[xScr/3.5,-yScr/6], text='5',height=fontH, color=textCol))
    
    #create text stimuli
    instructPrompt = visual.TextStim(win, height=fontH, color=textCol,
                                 pos=[0, yScr/10], wrapWidth=xScr/2)
    instructFirst = visual.TextStim(win, text="Press 5 to continue.",
                                height=fontH, color=textCol,
                                pos=[0, -yScr/4])
    instructMove = visual.TextStim(win,
                               text="Press 5 to continue, or 1 to go back.",
                               height=fontH, color=textCol,
                               pos=[0, -yScr/4])
    instructFinish = visual.TextStim(win,
                                 text="You have reached the end of the \
                                 instructions. When you are ready to \
                                 begin the first run, press any key.",
                                 height=fontH, color=textCol, pos=[0, 0],
                                 wrapWidth=xScr/3)
    wait = visual.TextStim(win, pos=[0, 0], text="Please wait momentarily. Your run will begin shortly.", 
                                 height=fontH, color=textCol)
    end = visual.TextStim(win, pos=[0, 0],text="You have now completed the experiment - thank you \
                                                        for your participation!", height=fontH)
    progress = visual.TextStim(win, pos=[0,0],height=fontH, color=textCol)
    
    #create jitter times
    jitter = []
    for x in range(31):
        jitter.append(0)
    for x in range(20):
        jitter.append(2.5)
    for x in range(7):
        jitter.append(5)
    for x in range(2):
        jitter.append(7.5)
    
    #present instructions
    if runNum == 0:
        forwardKey = "5"
        backKey = "1"
        endOfInstructions = False
        instructLine = 0
        while not endOfInstructions:
            instructPrompt.setText(instr[instructLine])
            instructPrompt.draw()
            if instructLine == 0:
                instructFirst.draw()
                win.flip()
                instructRep = event.waitKeys(keyList=[forwardKey])
            else:
                instructMove.draw()
                win.flip()
                instructRep = event.waitKeys(keyList=[forwardKey, backKey])
            if instructRep[0] == backKey:
                instructLine -= 1
            elif instructRep[0] == forwardKey:
                instructLine += 1
            if instr[instructLine] == "end":
                endOfInstructions = True
        instructFinish.draw()
        win.flip()
        event.waitKeys()
    wait.draw()
    win.flip()
    event.waitKeys(keyList = ['equal'])
    
    #loop through trials
    trialNum = 0
    runClock = core.Clock()
    trialClock = core.Clock()
    respTimeClock = core.Clock()
    
    while runNum < len(prefstim):
        counter = 0
        correctTimeToDate = 0
        random.shuffle(jitter)
        runClock.reset()
        while counter < len(pplstim):
            trialBegin = runClock.getTime()
            runs[runNum][counter][0].draw()
            win.flip()
            core.wait(1.0 - makeUpPerTrial)
            runs[runNum][counter][0].draw()
            runs[runNum][counter][1].draw()
            for x in range(5):
                ratings[x].setColor(textCol)
                scale[x].setColor(textCol)
                ratings[x].draw()
                scale[x].draw()
            win.flip()
            respTimeClock.reset()
            
            #collect and write results
            response = event.waitKeys(maxWait = 3.75 - makeUpPerTrial, keyList=['1','2','3','4','5', 'z'])
            respTime = respTimeClock.getTime()
            if response == ['z']:
                datafile.close()
                core.quit()
            if response != None:
                #show participant choice they selected
                ratings[int(response[0])-1].setColor([1,1,1])
                scale[int(response[0])-1].setColor([1,1,1])
                for x in range(5):
                    ratings[x].draw()
                    scale[x].draw()
                runs[runNum][counter][0].draw()
                runs[runNum][counter][1].draw()
                win.flip()
                core.wait(3.75 - respTime - makeUpPerTrial)
            else:
                response = ["NA"]
                respTime = "NA"
            
            #present fixation and jitter
            fix.draw()
            win.flip()
            core.wait(0.25 - makeUpPerTrial)
            trialDur = trialClock.getTime()
            trialJitterDur = trialDur + jitter[counter]
            output = [sn, runNum+1, trialNum+1, trialBegin, trialDur, 
                                    trialJitterDur, response[0], respTime, 
                                    runs[runNum][counter][0].text, index[runNum][counter][0], 
                                    runs[runNum][counter][1].text, index[runNum][counter][1]]
            writer.writerow(output)
            win.flip()
            #core.wait(jitter[counter] - makeUpPerTrial)
            
            #keep time on track
            correctTimeToDate += timePerTrial
            makeUpPerTrial = (runClock.getTime() - correctTimeToDate)/5
            
            trialNum += 1
            counter += 1
            trialClock.reset()
        win.flip()
        core.wait(5.0)
        
        #Shows progress in experiment
        if runNum < 11:
            progText = "You have finished " + str(runNum+1) + " out of 12 runs. Please press any key when you are ready to continue."
            progress.setText(progText)
            progress.draw()
            win.flip()
            event.waitKeys()
            wait.draw()
            win.flip()
            event.waitKeys(keyList=['equal'])
        runNum += 1
    #tell participants that they are done
    end.draw()
    win.flip()
    event.waitKeys(keyList = ['equal'])
    datafile.close()
    core.quit()
main()