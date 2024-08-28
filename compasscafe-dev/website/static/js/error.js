import * as THREE from 'https://cdn.skypack.dev/three@0.136.0';
import { GLTFLoader } from 'https://cdn.skypack.dev/three@0.136.0/examples/jsm/loaders/GLTFLoader.js';

// Error Page
let cupObject, smileObject, coffeeObject, outlineObject, coffeeText;
let mouseX = 0, mouseY = 0;

const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('errorcanvas'), antialias: true, alpha: true });
renderer.setClearColor(0x000000, 0);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);

const errorScene = new THREE.Scene();

// Master Group - Coffee Cup Error
const coffeeError = new THREE.Group();
errorScene.add(coffeeError);

// Point Light
const pointLight = new THREE.PointLight(0xffffff, 1.5, 150);
pointLight.position.set(-10, 20, 20);
errorScene.add(pointLight);

// Camera
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(8, 2, 20);
camera.lookAt(0, 0, 0);

// Fog
errorScene.fog = new THREE.FogExp2(0x5572c9, 0.03);

const loader = new GLTFLoader();

// Function to Apply Toon Material to Object
const applyToonMTL = (color) => {
    return new THREE.ShaderMaterial({
        uniforms: {
            uColor: { value: new THREE.Color(color) },
            uLightPosition: { value: pointLight.position },
            uAmbientLightColor: { value: new THREE.Color(0.3, 0.3, 0.3) }
        },
        vertexShader: `
            varying vec3 vNormal;
            varying vec3 vViewDir;
            varying vec3 vLightDir;

            uniform vec3 uLightPosition;

            void main() {
                vNormal = normalize(normalMatrix * normal);
                vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
                vViewDir = normalize(-mvPosition.xyz);
                vLightDir = normalize(uLightPosition - mvPosition.xyz); // Direction to the light
                gl_Position = projectionMatrix * mvPosition;
            }
        `,
        fragmentShader: `
            uniform vec3 uColor;
            uniform vec3 uAmbientLightColor;
            varying vec3 vNormal;
            varying vec3 vViewDir;
            varying vec3 vLightDir;

            void main() {
                vec3 normal = normalize(vNormal);
                vec3 lightDir = normalize(vLightDir);
                float NdotL = max(dot(normal, lightDir), 0.0);

                // Shadow Tint
                vec3 shadowColor = vec3(0.7, 0.8, 1.0);
                vec3 baseColor;

                // Light Level Controller
                if (NdotL > 0.7) {
                    baseColor = uColor; // Bright-Level Area
                } else if (NdotL > 0.4) {
                    baseColor = mix(uColor, shadowColor, 0.2); // Mid-Level Area
                } else if (NdotL > 0.2) {
                    baseColor = mix(uColor, shadowColor, 0.5); // Dark-Level Area
                } else {
                    baseColor = shadowColor; // Darker-Level Area
                }

                // Ambient Light
                vec3 finalColor = baseColor + uAmbientLightColor * 0.1;
                gl_FragColor = vec4(finalColor, 1.0);
            }
        `
    });
};

// Function to Apply Basic Material to Object
const applyBaseMTL = (color) => new THREE.MeshBasicMaterial({ color: color });

// LANDING PAGE COFFEE CUP MODEL GROUP

// Cup Base Model
loader.load('/static/assets/objects/cuppa-error/coffee-cup.glb', function(gltf) {
    cupObject = gltf.scene;
    cupObject.traverse(function (child) {
        if (child.isMesh) {
            // Toon Material
            child.material = applyToonMTL(0xffffff);
        }
    });

    // Add Cup Model to Group
    coffeeError.add(cupObject);

}, undefined, function(error) {
    console.error("Error loading base cup.", error);
});

// Outline Model
loader.load('/static/assets/objects/cuppa-error/coffee-outline.glb', function(gltf) {
    outlineObject = gltf.scene;
    outlineObject.traverse(function (child) {
        if (child.isMesh) {
            // Solid Material
            child.material = applyBaseMTL(0x000000);
        }
    });

    // Add Outline Model to Group
    coffeeError.add(outlineObject);

}, undefined, function(error) {
    console.error("Error loading outline.", error);
});

// Load the eyes (smile) model
loader.load('/static/assets/objects/cuppa-error/coffee-frown.glb', function(gltf) {
    smileObject = gltf.scene;

    smileObject.traverse(function (child) {
        if (child.isMesh) {
            // Solid Material
            child.material = applyBaseMTL(0x000000);
        }
    });

    // Add Smile Model to Group
    coffeeError.add(smileObject);

}, undefined, function(error) {
    console.error("Error loading face.", error);
});

// Load the coffee drink model
loader.load('/static/assets/objects/cuppa-error/coffee-drink.glb', function(gltf) {
    coffeeObject = gltf.scene;

    coffeeObject.traverse(function (child) {
        if (child.isMesh) {
            // Toon Material
            child.material = applyToonMTL(0x66381b);
        }
    });

    // Add Drink Model to Group
    coffeeError.add(coffeeObject);

}, undefined, function(error) {
    console.error("Error loading liquid.", error);
});

// Load the text model
loader.load('/static/assets/objects/cuppa-error/coffee-text.glb', function(gltf) {
    coffeeText = gltf.scene;

    coffeeText.traverse(function (child) {
        if (child.isMesh) {
            // Solid Material
            child.material = applyBaseMTL(0x232947);
            // Disable Fog
            child.material.fog = false;
        }
    });

    // Add Text Model to Group
    coffeeError.add(coffeeText);

}, undefined, function(error) {
    console.error("Error loading text.", error);
});



// Interactive 3D Viewport

// 3D Viewport Responsiveness
window.addEventListener('resize', onWindowResize);

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}


// Mouse Hover Interaction
let targetRotationX = 0;
let targetRotationY = 0;
let currentRotationX = 0;
let currentRotationY = 0;

const sensitivity = 0.15;
const dampingFactor = 0.05;

document.onmousemove = function(e) {
    mouseX = (e.clientX / window.innerWidth) * 2 - 1;
    mouseY = (e.clientY / window.innerHeight) * 2 - 1;

    targetRotationX = mouseY * sensitivity;
    targetRotationY = mouseX * sensitivity;
};

function animate() {
    // Render the scene
    currentRotationX = THREE.MathUtils.lerp(currentRotationX, targetRotationX, dampingFactor);
    currentRotationY = THREE.MathUtils.lerp(currentRotationY, targetRotationY, dampingFactor);

    // Rotate the entire error cup group instead of individual objects
    coffeeError.rotation.x = currentRotationX;
    coffeeError.rotation.y = currentRotationY;

    renderer.render(errorScene, camera);
    requestAnimationFrame(animate);
}

// Resize Coffee Group
coffeeError.scale.setScalar(8.5);
coffeeError.position.set(0, 0, 0);

animate();