-- Use the installed Gathering Storm panel and its normal end-turn and era UI.
include("ActionPanel_Expansion2.lua")

local refresh = OnRefresh
function OnRefresh()
    refresh()
    if not HasCapability("CAPABILITY_GOLDEN_AND_DARK_AGES") then
        Controls.AgeScoreContainer:SetHide(true)
    end
end
