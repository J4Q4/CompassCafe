import * as THREE from 'https://cdn.skypack.dev/three@0.136.0';
import { GLTFLoader } from 'https://cdn.skypack.dev/three@0.136.0/examples/jsm/loaders/GLTFLoader.js';
import { OutlineEffect } from 'https://cdn.skypack.dev/three@0.136.0/examples/jsm/effects/OutlineEffect.js';
import { OrbitControls } from 'https://cdn.skypack.dev/three@0.136.0/examples/jsm/controls/OrbitControls.js';

// Hero Landing Page
let cupObject, smileObject, coffeeObject;

const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('herocanvas'), antialias: true, alpha: true });
renderer.setClearColor(0x000000, 0);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);

const scene = new THREE.Scene();

// Master Group - Coffee Cup Hero
const coffeeHero = new THREE.Group();
scene.add(coffeeHero);

// Point Light
const pointLight = new THREE.PointLight(0xffffff, 1.5, 150);
pointLight.position.set(-10, 20, 20);
scene.add(pointLight);

// Camera
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 8, 20);
camera.lookAt(0, 0, 0);

// Orbit Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enablePan = true;

// Fog
scene.fog = new THREE.FogExp2(0x5572c9, 0.03);

const loader = new GLTFLoader();

// Function to Apply Basic Material to Object
const applyBaseMTL = (color) => new THREE.MeshBasicMaterial({ color: color });

const effect = new OutlineEffect(renderer, {
    defaultThickness: 0.01,
});

// LANDING PAGE COFFEE CUP MODEL GROUP

// Cup Base Model
loader.load('/static/assets/objects/cuppa-hero/coffee-cup.glb', function(gltf) {
    cupObject = gltf.scene;
    cupObject.traverse(function (child) {
        if (child.isMesh) {
            // Solid Material
            child.material = applyBaseMTL(0xffffff);
        }
    });

    // Add Cup Model to Group
    coffeeHero.add(cupObject);

}, undefined, function(error) {
    console.error("Error loading base cup.", error);
});

// Load the eyes (smile) model
loader.load('/static/assets/objects/cuppa-hero/coffee-smile.glb', function(gltf) {
    smileObject = gltf.scene;

    smileObject.traverse(function (child) {
        if (child.isMesh) {
            // Solid Material
            child.material = applyBaseMTL(0x000000);
        }
    });

    // Add Smile Model to Group
    coffeeHero.add(smileObject);

}, undefined, function(error) {
    console.error("Error loading face.", error);
});

// Load the coffee drink model
loader.load('/static/assets/objects/cuppa-hero/coffee-drink.glb', function(gltf) {
    coffeeObject = gltf.scene;

    coffeeObject.traverse(function (child) {
        if (child.isMesh) {
            // Solid Material
            child.material = applyBaseMTL(0x8B4513);
        }
    });

    // Add Drink Model to Group
    coffeeHero.add(coffeeObject);

}, undefined, function(error) {
    console.error("Error loading liquid.", error);
});

// 3D Viewport Responsiveness
window.addEventListener('resize', onWindowResize);

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    controls.update();
}

function animate() {
    // Render the scene
    controls.update();
    effect.render(scene, camera);
    requestAnimationFrame(animate);
}

// Resize Coffee Group
coffeeHero.scale.setScalar(6);
coffeeHero.position.set(0, -2, 0);

animate();
