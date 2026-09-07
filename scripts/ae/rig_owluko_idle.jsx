/**
 * Adobe After Effects Rigging Script for Owluko Idle Animation
 * Mascot: Owluko (Avian Porcelain Mascot)
 * Format: 512x512, 60.0 fps, 4.0s (240 frames)
 * 
 * Instructions:
 * 1. Open Adobe After Effects.
 * 2. Go to File > Scripts > Run Script File...
 * 3. Select this script file (rig_owluko_idle.jsx).
 * 4. The script creates the composition, imports all 11 isolated layers,
 *    configures sub-pixel anchor points, establishes the parenting hierarchy,
 *    and binds mathematical motion expressions for organic breathing,
 *    secondary wing hover, eyelid blinking, and ground shadow dynamics.
 */

(function rigOwlukoIdle() {
    app.beginUndoGroup("Rig Owluko Idle Animation");

    var compWidth = 512;
    var compHeight = 512;
    var pixelAspect = 1.0;
    var durationSec = 4.0;
    var fps = 60.0;

    // 1. Create or get Project & Composition
    var proj = app.project;
    if (!proj) {
        proj = app.newProject();
    }

    var comp = proj.items.addComp(
        "Owluko_Idle_Master_60fps",
        compWidth,
        compHeight,
        pixelAspect,
        durationSec,
        fps
    );
    comp.bgColor = [0, 0, 0];

    // Determine absolute path to rig_layers
    var scriptFile = new File($.fileName);
    var projectRoot = scriptFile.parent.parent.parent;
    var layersFolder = new Folder(projectRoot.fsName + "/mascots/owluko/rig_layers");

    if (!layersFolder.exists) {
        alert("Layers folder not found at: " + layersFolder.fsName);
        app.endUndoGroup();
        return;
    }

    // Layer specification table:
    // [filename, layerName, anchorX, anchorY, posX, posY, parentName]
    var layerSpecs = [
        ["00_shadow.png",         "01_Shadow",         256, 489, 256, 489, null],
        ["01_foot_left.png",      "02_Foot_Left",      204, 425, 204, 425, null],
        ["02_foot_right.png",     "03_Foot_Right",     308, 425, 308, 425, null],
        ["03_body_porcelain.png", "04_Body_Master",    256, 435, 256, 435, null],
        ["06_eye_left.png",       "05_Eye_Left",       193, 160, 193, 160, "04_Body_Master"],
        ["07_eye_right.png",      "06_Eye_Right",      315, 163, 315, 163, "04_Body_Master"],
        ["08_eyelid_left.png",    "07_Eyelid_Left",    193, 145, 193, 145, "04_Body_Master"],
        ["09_eyelid_right.png",   "08_Eyelid_Right",   315, 147, 315, 147, "04_Body_Master"],
        ["10_beak.png",           "09_Beak",           256, 175, 256, 175, "04_Body_Master"],
        ["04_wing_left.png",      "10_Wing_Left",      128, 192, 128, 192, "04_Body_Master"],
        ["05_wing_right.png",     "11_Wing_Right",     384, 192, 384, 192, "04_Body_Master"]
    ];

    var importedLayers = {};

    // 2. Import footage and place in comp
    for (var i = 0; i < layerSpecs.length; i++) {
        var spec = layerSpecs[i];
        var fName = spec[0];
        var lName = spec[1];
        var ax = spec[2];
        var ay = spec[3];
        var px = spec[4];
        var py = spec[5];

        var file = new File(layersFolder.fsName + "/" + fName);
        if (!file.exists) {
            alert("Missing layer asset: " + file.fsName);
            continue;
        }

        var io = new ImportOptions(file);
        var footageItem = proj.importFile(io);
        var avLayer = comp.layers.add(footageItem);
        avLayer.name = lName;

        // Set Anchor Point and Position
        avLayer.property("ADBE Transform Group").property("ADBE Anchor Point").setValue([ax, ay]);
        avLayer.property("ADBE Transform Group").property("ADBE Position").setValue([px, py]);

        importedLayers[lName] = avLayer;
    }

    // 3. Establish Parenting Hierarchy
    for (var j = 0; j < layerSpecs.length; j++) {
        var spec = layerSpecs[j];
        var lName = spec[1];
        var parentName = spec[6];
        if (parentName && importedLayers[lName] && importedLayers[parentName]) {
            importedLayers[lName].parent = importedLayers[parentName];
        }
    }

    // 4. Bind Organic Expressions

    // 4A. Body Master: Organic Breathing (Squash & Stretch) + Subtle Pelvis Float + Head Tilt
    if (importedLayers["04_Body_Master"]) {
        var bodyLayer = importedLayers["04_Body_Master"];
        
        // Scale Expression (Organic Respiratory Loop: period = 2.0s, 2 full breaths per 4s loop)
        var scaleExpr = 
            "var freq = 0.5;\n" +
            "var breath = Math.sin(time * 2 * Math.PI * freq);\n" +
            "var sy = 100 + breath * 1.8;\n" +
            "var sx = 100 - breath * 0.9;\n" +
            "[sx, sy];";
        bodyLayer.property("ADBE Transform Group").property("ADBE Scale").expression = scaleExpr;

        // Position Float (Subtle vertical displacement matching breathing)
        var posExpr = 
            "var freq = 0.5;\n" +
            "var breath = Math.sin(time * 2 * Math.PI * freq);\n" +
            "var dy = breath * 1.6;\n" +
            "[value[0], value[1] + dy];";
        bodyLayer.property("ADBE Transform Group").property("ADBE Position").expression = posExpr;

        // Inquisitive Owl Micro-tilt (period = 4.0s)
        var rotExpr = 
            "var freq = 0.25;\n" +
            "var tilt = Math.sin(time * 2 * Math.PI * freq) * 1.6;\n" +
            "value + tilt;";
        bodyLayer.property("ADBE Transform Group").property("ADBE Rotate Z").expression = rotExpr;
    }

    // 4B. Wings: Secondary Harmonic Float with Phase Lag (Drag & Lift)
    if (importedLayers["10_Wing_Left"]) {
        var wLeft = importedLayers["10_Wing_Left"];
        var wLeftExpr = 
            "var freq = 0.5;\n" +
            "var phaseLag = 0.12;\n" +
            "var sway = Math.sin((time - phaseLag) * 2 * Math.PI * freq) * -2.4;\n" +
            "value + sway;";
        wLeft.property("ADBE Transform Group").property("ADBE Rotate Z").expression = wLeftExpr;
    }

    if (importedLayers["11_Wing_Right"]) {
        var wRight = importedLayers["11_Wing_Right"];
        var wRightExpr = 
            "var freq = 0.5;\n" +
            "var phaseLag = 0.12;\n" +
            "var sway = Math.sin((time - phaseLag) * 2 * Math.PI * freq) * 2.4;\n" +
            "value + sway;";
        wRight.property("ADBE Transform Group").property("ADBE Rotate Z").expression = wRightExpr;
    }

    // 4C. Ground Shadow: Harmonic Expansion synchronized with Body Squash
    if (importedLayers["01_Shadow"]) {
        var shadowLayer = importedLayers["01_Shadow"];
        var shadowScaleExpr = 
            "var freq = 0.5;\n" +
            "var breath = Math.sin(time * 2 * Math.PI * freq);\n" +
            "var s = 100 + breath * 1.4;\n" +
            "[s, s];";
        shadowLayer.property("ADBE Transform Group").property("ADBE Scale").expression = shadowScaleExpr;
    }

    // 4D. Eyelids: Keyframed Natural Blink Cycle
    // Blinks at t = 1.2s and t = 3.1s
    function applyBlinkKeyframes(eyelidLayer) {
        var posProp = eyelidLayer.property("ADBE Transform Group").property("ADBE Position");
        var basePos = posProp.value;
        var blinkOffset = 16.0; // downwards translation covering the amber iris

        // Keyframe 1: Start Blink 1 at t = 1.15s
        posProp.setValueAtTime(1.15, basePos);
        // Keyframe 2: Fully closed at t = 1.23s
        posProp.setValueAtTime(1.23, [basePos[0], basePos[1] + blinkOffset]);
        // Keyframe 3: Re-open at t = 1.32s
        posProp.setValueAtTime(1.32, basePos);

        // Keyframe 4: Start Blink 2 at t = 3.05s
        posProp.setValueAtTime(3.05, basePos);
        // Keyframe 5: Fully closed at t = 3.13s
        posProp.setValueAtTime(3.13, [basePos[0], basePos[1] + blinkOffset]);
        // Keyframe 6: Re-open at t = 3.22s
        posProp.setValueAtTime(3.22, basePos);
    }

    if (importedLayers["07_Eyelid_Left"]) {
        applyBlinkKeyframes(importedLayers["07_Eyelid_Left"]);
    }
    if (importedLayers["08_Eyelid_Right"]) {
        applyBlinkKeyframes(importedLayers["08_Eyelid_Right"]);
    }

    // 4E. Eyes: Inquisitive Gaze Shift Saccade
    function applyGazeKeyframes(eyeLayer) {
        var posProp = eyeLayer.property("ADBE Transform Group").property("ADBE Position");
        var basePos = posProp.value;
        
        posProp.setValueAtTime(0.0, basePos);
        posProp.setValueAtTime(1.8, basePos);
        // Shift gaze slightly left and down at t = 2.0s
        posProp.setValueAtTime(2.0, [basePos[0] - 2.0, basePos[1] + 1.0]);
        posProp.setValueAtTime(2.8, [basePos[0] - 2.0, basePos[1] + 1.0]);
        // Return to center at t = 3.0s
        posProp.setValueAtTime(3.0, basePos);
        posProp.setValueAtTime(4.0, basePos);
    }

    if (importedLayers["05_Eye_Left"]) {
        applyGazeKeyframes(importedLayers["05_Eye_Left"]);
    }
    if (importedLayers["06_Eye_Right"]) {
        applyGazeKeyframes(importedLayers["06_Eye_Right"]);
    }

    app.endUndoGroup();
    alert("Owluko Rigging Complete! Comp: 'Owluko_Idle_Master_60fps' (512x512, 60fps, 4.0s)");
})();
