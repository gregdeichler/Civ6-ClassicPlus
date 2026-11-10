-- The stock hook checks CAPABILITY_ERAS alone. Keep eras and gate the age screen.
include("PartialScreenHooks_Expansion2")

local addEraHook = AddEraHook
function AddEraHook()
    if HasCapability("CAPABILITY_GOLDEN_AND_DARK_AGES") then
        addEraHook()
    end
end
