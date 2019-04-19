#!/usr/bin/python

# Authors: Christoph Hohner (D051874), Nena Raab (D048418)                                 #
# ---------------------------------------------------------------------------------------  #
# Preparation Steps (manual)                                                               #
# ---------------------------------------------------------------------------------------  #
# First make sure that the updates are provided on remote GitHub!                          #
#                                                                                          #
# Then (within rebase folder) do                                                           #
# git clone git@github.wdf.sap.corp:cc-java/cc-bulletinboard-ads-spring-webmvc.git         #
#                                                                                          #
# It checks out all branches and detects whether there is a rebase required and            #
#   if there are no additional commits that needs to be squashed it automatically rebases. #
# ---------------------------------------------------------------------------------------  #
# Execute using python rebase-helper.py                                                    #
# ---------------------------------------------------------------------------------------  #
# Postprocessing Steps (manual)                                                            #
# ---------------------------------------------------------------------------------------  #
# Please check final result (local branches) using 'gitk --all'                            #
# At the end, you can push using `git push -f --all`                                       #
# -----------------------------------------------------------------------------------------#

# -----IMPORTS
import subprocess
import os
import sys

# -----FUNCTIONS
def checkout (branches):
    for i in range(len(branches)):
        subprocess.check_output([ "git", "checkout", "-q", branches[i] ])

def rebase (branches):
    updating = False
    rebase_counter = 0
    rebase_interactive = 0
    
    for i in range(len(branches) - 1):
        parent = branches[i]
        current = branches[i + 1]
    
        print "=== ('%i') Rebase current '%s' on parent '%s'" % (i + 1 , current, parent)
    
        changes = subprocess.check_output([ "git", "log", "--oneline", "%s..%s" % (parent, current) ])
        changes = changes.strip().splitlines()
        if not updating:
            if len(changes) > 1:
                updating = True
            else:
                print "> ------------ > nothing to to "
                continue
        subprocess.check_call([ "git", "checkout", "-q", current ])
    
        changes = subprocess.check_output([ "git", "log", "--oneline", "origin/%s..%s" % (parent, current) ])
        changes = changes.strip().splitlines()
        onlyone = len(changes) == 1
        if onlyone:
            # just one pick -> does not need to be interactive
            interactive_flag = []
            rebase_counter += 1
        else:
            interactive_flag = [ "-i" ]
            rebase_interactive += 1
            rebase_counter += 1
    
        print "> ------------ > updating branch '%s' '%s' ------------" % (current, interactive_flag)
        subprocess.check_call([ "git", "rebase" ] + interactive_flag + [ "--onto", parent, "origin/" + parent, current ])
    
    print "Statistics: number of branches rebased: '%i' (interactively rebased: '%i') " % (rebase_counter, rebase_interactive)
    print "*****************************************************************************"


# -----VARIABLES

# -----BRANCHES (Update this branches if necessary)
# The 'solution-pre-exercises' branch is left untouched, rebase manually if necessary.  
branches = [
    "initial",
    "master",
    "solution-1-Activate-Actuator",
    "solution-2-Hello-World-Resource",
    "solution-3-Create-Ads-Endpoints",
    "exercise-4-Create-ServiceTests",
    "solution-4-Create-ServiceTests",
    "solution-4-2-DeleteUpdate",
    "solution-5-ValidationExceptions",
    "solution-6-Deploy-Ads-On-CF",
    "solution-8-1-Configure-Persistence",
    "solution-8-2-Use-Repository-To-Access-Database",
    "solution-8-3-IntroducePaging",
    "solution-9-Implement-JPA-Entity",
    "solution-9-2-Introduce-Data-Transfer-Object-DTO",
    "solution-10-Deploy-Ads-With-DB-Service-On-CF",
    "solution-11-Develop-Custom-Queries",
    "solution-12-Setup-Logger",
    "solution-13-Use-SLF4J-Features",
    "solution-14-Bind-Application-Logs-Service",
    "solution-16-Call-User-Service",
    "solution-17-Integrate-Hystrix",
    "exercise-18-Make-Communication-Resilient",
    "solution-18-Make-Communication-Resilient",
    "solution-18-2-Make-Fallback-Configurable-using-Lambda",
    "solution-19-Transfer-CorrelationID",
    "solution-19-2-Springify-Hystrix-Command",
    "solution-20-Use-Message-Queues",
    "solution-21-Receive-MQ-Messages",
    "solution-22-Deploy-AppRouter",
    "solution-23-Setup-Generic-Authorization",
    "solution-24-Make-App-Secure",
    "solution-25-Make-App-TenantAware"
]

demo_sapui_branches = [
    "solution-6-Deploy-Ads-On-CF",
    "demo-sapui5"
]

demo_aop_branches = [
    "solution-19-2-Springify-Hystrix-Command",
    "demo-aop-for-logging"
]

demo_redis_branches = [
    "solution-19-2-Springify-Hystrix-Command",
    "demo-redis"
]


# ------Step 1: initialize
githome = "./git/rebase"
gitfolder = githome + "/cc-bulletinboard-ads-spring-webmvc"

if len(sys.argv) is 1:
    os.chdir("cc-bulletinboard-ads-spring-webmvc")
    checkout(branches)
    checkout(demo_sapui_branches)
    checkout(demo_aop_branches)
    checkout(demo_redis_branches)


# ------Step 2: rebase
rebase(branches)
rebase(demo_sapui_branches)
rebase(demo_aop_branches)
rebase(demo_redis_branches)

# ------The End
print "Navigate into git folder 'cd %s'" % gitfolder
print "Please check final result (local branches) using 'gitk --all' "
print "Finally you can overwrite the remote branches using 'git push -f --all' "