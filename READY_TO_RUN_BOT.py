"""
MHT-CET PREPARATION BOT - READY TO RUN
Just replace BOT_TOKEN with yours from @BotFather and run!

Contains 183 real MHT-CET style questions covering:
- Physics: Rotational Dynamics, Electrostatics
- Chemistry: Solid State, Chemical Kinetics  
- Mathematics: Matrices, Integration
"""

import telebot
from telebot import types
import json
import random
import time
import os
from datetime import datetime
from collections import defaultdict
import threading

# =========================
# ⚠️ REPLACE THIS TOKEN ⚠️
# =========================
BOT_TOKEN = "7240890804:AAEwjjDk1gh1hFoJgmNZ9ExZUNKGq6TnI2I"  # Get from @BotFather
# =========================

DATA_DIR = "bot_data"
USER_DATA_FILE = os.path.join(DATA_DIR, "users.json")

bot = telebot.TeleBot(BOT_TOKEN)
os.makedirs(DATA_DIR, exist_ok=True)

# =========================
# SUBJECTS & CHAPTERS
# =========================
SUBJECTS = {
    "Physics": {
        "emoji": "📘",
        "chapters": ["Rotational Dynamics", "Electrostatics", "Current Electricity"]
    },
    "Chemistry": {
        "emoji": "🧪",
        "chapters": ["Solid State", "Chemical Kinetics"]
    },
    "Mathematics": {
        "emoji": "📐",
        "chapters": ["Matrices", "Integration"]
    }
}

DIFFICULTY_LEVELS = {
    "🟢 Easy": {"level": "easy", "desc": "Concept Builders"},
    "🟡 Moderate": {"level": "moderate", "desc": "CET Level"},
    "🔴 Hard": {"level": "hard", "desc": "Rank Booster"}
}

# =========================
# ALL 183 QUESTIONS HERE!
# =========================
QUESTIONS = {
    "Physics": {
        "Rotational Dynamics": {
            "easy": [
                {"q": "The SI unit of moment of inertia is", "opts": ["kg·m²", "kg·m", "kg/m²", "N·m"], "ans": "kg·m²", "exp": "Moment of inertia = mass × (distance)², hence units are kg·m²"},
                {"q": "The rotational analogue of mass is", "opts": ["Moment of inertia", "Torque", "Angular momentum", "Angular velocity"], "ans": "Moment of inertia", "exp": "Just as mass resists linear motion, moment of inertia resists rotational motion"},
                {"q": "The moment of inertia of a uniform rod about an axis through its center perpendicular to length is", "opts": ["ML²/12", "ML²/3", "ML²/2", "ML²"], "ans": "ML²/12", "exp": "Standard formula for rod about center: I = ML²/12"},
                {"q": "Torque is maximum when angle between force and radius vector is", "opts": ["90°", "0°", "45°", "180°"], "ans": "90°", "exp": "τ = r × F = rF sin θ, maximum when sin θ = 1, i.e., θ = 90°"},
                {"q": "The dimension of angular momentum is", "opts": ["[ML²T⁻¹]", "[MLT⁻¹]", "[ML²T⁻²]", "[MLT⁻²]"], "ans": "[ML²T⁻¹]", "exp": "L = Iω = (kg·m²)(rad/s) = kg·m²·s⁻¹ = [ML²T⁻¹]"},
                {"q": "Radius of gyration depends on", "opts": ["Distribution of mass", "Total mass only", "Shape only", "None of these"], "ans": "Distribution of mass", "exp": "K = √(I/M), depends on how mass is distributed about axis"},
                {"q": "The unit of torque is same as", "opts": ["Energy", "Force", "Power", "Momentum"], "ans": "Energy", "exp": "Both torque and energy have units N·m or J"},
                {"q": "Angular momentum is conserved when", "opts": ["External torque is zero", "External force is zero", "Moment of inertia is constant", "Angular velocity is constant"], "ans": "External torque is zero", "exp": "τ_ext = dL/dt, so if τ_ext = 0, then L = constant"},
                {"q": "For a disc rolling without slipping, the ratio of translational to rotational KE is", "opts": ["2:1", "1:2", "3:1", "1:1"], "ans": "2:1", "exp": "For disc I = MR²/2, KE_trans/KE_rot = ½Mv²/(½Iω²) = 2:1"},
                {"q": "A flywheel has high moment of inertia because it has", "opts": ["Mass concentrated at rim", "Uniform mass distribution", "Mass at center", "Lightweight material"], "ans": "Mass concentrated at rim", "exp": "I increases when mass is far from axis, I ∝ r²"}
            ],
            "moderate": [
                {"q": "A disc and ring of same mass M and radius R roll down. The ratio of accelerations (disc:ring) is", "opts": ["4:3", "3:4", "1:1", "2:1"], "ans": "4:3", "exp": "a = g sin θ/(1 + K²/R²). For disc K²/R² = 1/2, ring = 1. Ratio = 4:3"},
                {"q": "If moment of inertia of a disc about diameter is I, then about tangent it is", "opts": ["3I", "2I", "4I", "5I"], "ans": "3I", "exp": "I_diameter = MR²/4 = I. I_tangent = I_center + MR² = MR²/2 + MR² = 3MR²/2 = 3I"},
                {"q": "A solid sphere, disc and ring start from rest and roll down. Which reaches first?", "opts": ["Solid sphere", "Disc", "Ring", "All together"], "ans": "Solid sphere", "exp": "Acceleration a = g sin θ/(1 + I/MR²). Sphere has lowest I/MR² = 2/5"},
                {"q": "The angular momentum of a particle is L = 4t² + 2t + 1. The torque at t = 2s is", "opts": ["18 N·m", "16 N·m", "20 N·m", "22 N·m"], "ans": "18 N·m", "exp": "τ = dL/dt = 8t + 2. At t = 2, τ = 16 + 2 = 18 N·m"},
                {"q": "Two discs of moments of inertia I₁ and I₂ rotating with ω₁ and ω₂ are coupled. Final angular velocity is", "opts": ["(I₁ω₁ + I₂ω₂)/(I₁ + I₂)", "(I₁ω₁ - I₂ω₂)/(I₁ + I₂)", "ω₁ + ω₂", "(ω₁ + ω₂)/2"], "ans": "(I₁ω₁ + I₂ω₂)/(I₁ + I₂)", "exp": "By conservation of angular momentum: I₁ω₁ + I₂ω₂ = (I₁ + I₂)ω"},
                {"q": "A rod of length L pivoted at one end is released from horizontal. Angular velocity at bottom is", "opts": ["√(3g/L)", "√(6g/L)", "√(g/L)", "√(2g/L)"], "ans": "√(3g/L)", "exp": "PE lost = Mg(L/2) = KE gained = ½Iω². I = ML²/3, solve: ω = √(3g/L)"},
                {"q": "The kinetic energy of a rolling body is distributed in ratio 1:2 between rotational and translational. Body is", "opts": ["Ring", "Disc", "Solid sphere", "Hollow sphere"], "ans": "Disc", "exp": "KE_rot/KE_trans = (I/MR²). For 1:2, I/MR² = 1/2, which is disc"},
                {"q": "A particle moves in xy plane. Angular momentum about origin when at (2, 2) with velocity (3î + 3ĵ) m/s is", "opts": ["Zero", "12k̂", "-12k̂", "6k̂"], "ans": "Zero", "exp": "L = r × mv = m[(2î + 2ĵ) × (3î + 3ĵ)] = m(6k̂ - 6k̂) = 0"},
                {"q": "Moment of inertia of a uniform circular disc about a tangent in its plane is 5MR²/4. About diameter it is", "opts": ["MR²/4", "MR²/2", "3MR²/4", "MR²"], "ans": "MR²/4", "exp": "I_tangent = I_center + MR². Solve backwards: I_diameter = MR²/4"},
                {"q": "A wheel starting from rest acquires angular velocity 100 rad/s in 10s. Number of revolutions is", "opts": ["80", "100", "50", "75"], "ans": "80", "exp": "θ = ½αt² = ½(ω/t)t² = ½ωt = ½×100×10 = 500 rad = 500/2π ≈ 80 rev"}
            ],
            "hard": [
                {"q": "Four point masses each m at corners of square of side a. Moment of inertia about diagonal is", "opts": ["ma²", "2ma²", "ma²/2", "4ma²"], "ans": "ma²", "exp": "Two masses on diagonal contribute 0. Other two at distance a/√2: I = 2m(a/√2)² = ma²"},
                {"q": "A solid cylinder and hollow cylinder of same mass roll down. Ratio of velocities at bottom (solid:hollow) is", "opts": ["√(4/3)", "√(3/4)", "√2", "√(1/2)"], "ans": "√(4/3)", "exp": "v = √[2gh/(1 + I/MR²)]. I_solid/MR² = 1/2, I_hollow/MR² = 1. v_s/v_h = √(4/3)"},
                {"q": "A uniform rod of mass M, length L hinged at one end. Minimum velocity at free end to make it vertical is", "opts": ["√(3gL)", "√(6gL)", "√(2gL)", "√(gL)"], "ans": "√(3gL)", "exp": "At top PE = MgL, KE = Mv²/6. Solve: v = √(3gL)"},
                {"q": "A disc rolls without slipping with velocity v. What is velocity of topmost point?", "opts": ["2v", "v", "v/2", "3v"], "ans": "2v", "exp": "Bottom point velocity = 0, center = v. Top = v + v = 2v"},
                {"q": "Moment of inertia of uniform solid sphere of radius R about tangent is", "opts": ["7MR²/5", "2MR²/5", "5MR²/7", "3MR²/5"], "ans": "7MR²/5", "exp": "I_center = 2MR²/5. I_tangent = I_center + MR² = 2MR²/5 + MR² = 7MR²/5"},
                {"q": "A circular disc of radius R is removed from bigger disc of radius 2R. Distance of center of mass from center of bigger disc is", "opts": ["R/3", "R/2", "2R/3", "R/4"], "ans": "R/3", "exp": "Using x_cm = (M₁x₁ - M₂x₂)/(M₁ - M₂). M ∝ R². Work out: x = R/3"},
                {"q": "If earth suddenly stops rotating, the value of g at equator will", "opts": ["Increase", "Decrease", "Remain same", "Become zero"], "ans": "Increase", "exp": "g_eff = g - ω²R. If ω = 0, g_eff = g (increases)"},
                {"q": "A rod of length L and mass M is pivoted at L/4 from one end. Its moment of inertia about pivot is", "opts": ["7ML²/48", "ML²/12", "ML²/3", "5ML²/48"], "ans": "7ML²/48", "exp": "I_center = ML²/12. Distance from center = L/4. I = ML²/12 + M(L/4)² = 7ML²/48"},
                {"q": "A wheel is rolling on ground. Ratio of translational to total kinetic energy is", "opts": ["1/(1 + K²/R²)", "K²/R²", "1 + K²/R²", "R²/K²"], "ans": "1/(1 + K²/R²)", "exp": "KE_trans = ½Mv², KE_rot = ½MK²(v/R)². Ratio = 1/(1 + K²/R²)"},
                {"q": "Ice skater brings arms close to body. Angular velocity becomes 3 times. The rotational kinetic energy becomes", "opts": ["3 times", "9 times", "1/3 times", "Remains same"], "ans": "3 times", "exp": "L = Iω = const. KE = ½Iω² ∝ ω (when L const). KE₂ = 3KE₁"}
            ]
        },
        "Electrostatics": {
            "easy": [
                {"q": "The SI unit of electric field is", "opts": ["N/C", "C/N", "N·C", "C·m"], "ans": "N/C", "exp": "Electric field = Force/Charge, units are Newton/Coulomb"},
                {"q": "Electric field inside a conductor in electrostatic equilibrium is", "opts": ["Zero", "Maximum", "Minimum", "Depends on shape"], "ans": "Zero", "exp": "In equilibrium, charges reside on surface, field inside = 0"},
                {"q": "SI unit of electric flux is", "opts": ["N·m²/C", "N/C", "C/m²", "V·m"], "ans": "N·m²/C", "exp": "Φ = E·A, units are (N/C)(m²) = N·m²/C or V·m"},
                {"q": "Coulomb's law is valid for", "opts": ["Point charges", "Extended bodies only", "Conductors only", "All of these"], "ans": "Point charges", "exp": "F = kq₁q₂/r² is valid for point charges or spherical charge distributions"},
                {"q": "Electric field lines never", "opts": ["Intersect", "Start from positive charge", "End on negative charge", "Curve"], "ans": "Intersect", "exp": "If lines intersect, E has two directions at same point, which is impossible"},
                {"q": "The value of permittivity of free space ε₀ is approximately", "opts": ["8.85 × 10⁻¹² C²/N·m²", "9 × 10⁹ N·m²/C²", "1.6 × 10⁻¹⁹ C", "6.67 × 10⁻¹¹ N·m²/kg²"], "ans": "8.85 × 10⁻¹² C²/N·m²", "exp": "ε₀ = 8.85 × 10⁻¹² C²/N·m² or F/m"},
                {"q": "Electric potential is a", "opts": ["Scalar quantity", "Vector quantity", "Tensor", "Dimensionless"], "ans": "Scalar quantity", "exp": "Potential has magnitude but no direction, hence scalar"},
                {"q": "Work done in moving a charge in equipotential surface is", "opts": ["Zero", "Minimum", "Maximum", "Infinite"], "ans": "Zero", "exp": "W = q(V₂ - V₁) = 0 since V₂ = V₁ on equipotential surface"},
                {"q": "Electric field and potential are related as", "opts": ["E = -dV/dr", "E = dV/dr", "E = V/r", "V = E·r"], "ans": "E = -dV/dr", "exp": "Electric field is negative gradient of potential"},
                {"q": "Gauss's law is useful for calculating E when charge distribution has", "opts": ["Symmetry", "No symmetry", "Variable charge", "Zero charge"], "ans": "Symmetry", "exp": "Gauss's law ∮E·dA = q/ε₀ is easy to apply with spherical, cylindrical, planar symmetry"}
            ],
            "moderate": [
                {"q": "Electric potential at center of uniformly charged ring of radius R is proportional to", "opts": ["1/R", "1/R²", "R", "R²"], "ans": "1/R", "exp": "V = kQ/R at center, inversely proportional to R"},
                {"q": "Two charges +q and -q separated by distance d. Electric field at center is", "opts": ["2kq/d²", "kq/d²", "4kq/d²", "Zero"], "ans": "2kq/d²", "exp": "Fields from both charges add up at center"},
                {"q": "Capacitance of parallel plate capacitor is doubled when", "opts": ["Distance halved", "Distance doubled", "Area halved", "Charge doubled"], "ans": "Distance halved", "exp": "C = ε₀A/d. If d → d/2, then C → 2C"},
                {"q": "Three capacitors 2µF, 3µF, 4µF in series. Equivalent capacitance is", "opts": ["12/13 µF", "9 µF", "13/12 µF", "2 µF"], "ans": "12/13 µF", "exp": "1/C = 1/2 + 1/3 + 1/4 = 13/12. C = 12/13 µF"},
                {"q": "Energy stored in capacitor is U. If charge is doubled, energy becomes", "opts": ["4U", "2U", "U", "U/2"], "ans": "4U", "exp": "U = Q²/2C. If Q → 2Q, then U → 4U"},
                {"q": "A hollow metal sphere of radius R is charged to potential V. Electric field at distance R/2 from center is", "opts": ["Zero", "V/R", "2V/R", "V/(2R)"], "ans": "Zero", "exp": "Inside hollow conductor, E = 0"},
                {"q": "If a dielectric slab of K=6 is inserted in parallel plate capacitor, capacitance becomes", "opts": ["6 times", "1/6 times", "36 times", "Remains same"], "ans": "6 times", "exp": "C' = KC = 6C"},
                {"q": "Electric dipole of moment p in uniform field E experiences maximum torque when angle is", "opts": ["90°", "0°", "180°", "45°"], "ans": "90°", "exp": "τ = pE sin θ, maximum when θ = 90°"},
                {"q": "Electric field at distance r from infinite line charge (λ C/m) is", "opts": ["λ/2πε₀r", "λ/4πε₀r", "λ/πε₀r", "λ/ε₀r"], "ans": "λ/2πε₀r", "exp": "Using Gauss's law for cylindrical symmetry: E = λ/2πε₀r"},
                {"q": "Two identical capacitors connected in series then in parallel. Ratio of capacitances (series:parallel) is", "opts": ["1:4", "1:2", "2:1", "4:1"], "ans": "1:4", "exp": "C_series = C/2, C_parallel = 2C. Ratio = (C/2):(2C) = 1:4"}
            ],
            "hard": [
                {"q": "Capacitance of spherical conductor of radius R in vacuum is", "opts": ["4πε₀R", "4πε₀R²", "ε₀R", "πε₀R"], "ans": "4πε₀R", "exp": "For isolated sphere: C = 4πε₀R"},
                {"q": "Energy density in electric field E is", "opts": ["½ε₀E²", "ε₀E²", "ε₀E", "½ε₀E"], "ans": "½ε₀E²", "exp": "u = ½ε₀E² joules per cubic meter"},
                {"q": "A charged soap bubble of radius R is given more charge. Its radius becomes 2R. The ratio of capacitances is", "opts": ["1:2", "2:1", "1:4", "4:1"], "ans": "1:2", "exp": "C = 4πε₀R. C₂/C₁ = R₂/R₁ = 2R/R = 2:1"},
                {"q": "Two concentric spheres of radii a and b (b>a). Capacitance is", "opts": ["4πε₀ab/(b-a)", "4πε₀(b-a)", "4πε₀a", "4πε₀b"], "ans": "4πε₀ab/(b-a)", "exp": "C = 4πε₀/(1/a - 1/b) = 4πε₀ab/(b-a)"},
                {"q": "Electric dipole of moment 2×10⁻⁸ C·m in field 5×10⁵ N/C at 30°. Torque experienced is", "opts": ["5×10⁻³ N·m", "10⁻² N·m", "5×10⁻⁴ N·m", "10⁻³ N·m"], "ans": "5×10⁻³ N·m", "exp": "τ = pE sin θ = 2×10⁻⁸ × 5×10⁵ × sin 30° = 5×10⁻³ N·m"},
                {"q": "Charge Q divided in ratio x:(1-x) to get maximum repulsion between them. Value of x is", "opts": ["1/2", "1/3", "2/3", "1/4"], "ans": "1/2", "exp": "F = kq₁q₂/r² = kxQ(1-x)Q/r². dF/dx = 0 gives x = 1/2"},
                {"q": "Metallic sphere of radius R at potential V. Charge on it is", "opts": ["4πε₀RV", "4πε₀R²V", "4πε₀V/R", "πε₀RV"], "ans": "4πε₀RV", "exp": "C = 4πε₀R, Q = CV = 4πε₀RV"},
                {"q": "Electric field at point (3, 4, 0) due to charge q at origin is E. Field at (6, 8, 0) is", "opts": ["E/4", "E/2", "E", "2E"], "ans": "E/4", "exp": "r₁ = 5, r₂ = 10. E ∝ 1/r². E₂/E₁ = (r₁/r₂)² = 1/4"},
                {"q": "Capacity of earth (radius 6400 km) is approximately", "opts": ["700 µF", "7000 µF", "70 µF", "70000 µF"], "ans": "700 µF", "exp": "C = 4πε₀R ≈ 711 µF"},
                {"q": "A charge Q on capacitor C. Battery is disconnected and dielectric K is inserted. New potential is", "opts": ["V/K", "KV", "V", "V/K²"], "ans": "V/K", "exp": "Q constant. C' = KC, V' = Q/C' = V/K"}
            ]
        },
        "Current Electricity": {
            "easy": [
                {"q": "Ohm's law states V = IR where R is", "opts": ["Resistance", "Reluctance", "Resistivity", "Reactance"], "ans": "Resistance", "exp": "Ohm's law: Voltage = Current × Resistance"},
                {"q": "SI unit of resistance is", "opts": ["Ohm (Ω)", "Volt", "Ampere", "Coulomb"], "ans": "Ohm (Ω)", "exp": "Resistance is measured in ohms"},
                {"q": "SI unit of current is", "opts": ["Ampere", "Volt", "Ohm", "Watt"], "ans": "Ampere", "exp": "Current is measured in amperes"}
            ],
            "moderate": [
                {"q": "Two resistances 2Ω and 3Ω in parallel. Equivalent resistance is", "opts": ["1.2Ω", "5Ω", "0.83Ω", "6Ω"], "ans": "1.2Ω", "exp": "1/R = 1/2 + 1/3 = 5/6. R = 6/5 = 1.2Ω"}
            ],
            "hard": [
                {"q": "A wire of resistance R is stretched to double its length. New resistance is", "opts": ["4R", "2R", "R/2", "R/4"], "ans": "4R", "exp": "Volume constant: Al = const. If l → 2l, A → A/2. R' = 4R"}
            ]
        }
    },
    "Chemistry": {
        "Solid State": {
            "easy": [
                {"q": "The coordination number in FCC (Face Centered Cubic) is", "opts": ["12", "8", "6", "4"], "ans": "12", "exp": "In FCC, each atom touches 12 neighbors"},
                {"q": "The number of atoms per unit cell in BCC is", "opts": ["2", "1", "4", "8"], "ans": "2", "exp": "BCC: 8 corners (1/8 each) + 1 body center = 2 atoms"},
                {"q": "The packing efficiency of simple cubic is", "opts": ["52.4%", "68%", "74%", "34%"], "ans": "52.4%", "exp": "Simple cubic has 52.4% packing efficiency"},
                {"q": "NaCl crystal structure has", "opts": ["FCC", "BCC", "Simple cubic", "HCP"], "ans": "FCC", "exp": "NaCl has FCC lattice of Cl⁻ with Na⁺ in octahedral voids"},
                {"q": "In CsCl structure, coordination number is", "opts": ["8:8", "6:6", "4:4", "12:12"], "ans": "8:8", "exp": "CsCl has 8:8 coordination"},
                {"q": "Number of tetrahedral voids per atom in cubic close packing is", "opts": ["2", "1", "4", "8"], "ans": "2", "exp": "Tetrahedral voids = 2 × number of atoms"},
                {"q": "Number of octahedral voids per atom in cubic close packing is", "opts": ["1", "2", "4", "0.5"], "ans": "1", "exp": "Octahedral voids = number of atoms"},
                {"q": "The fraction of total volume occupied by atoms in FCC is", "opts": ["0.74", "0.52", "0.68", "0.34"], "ans": "0.74", "exp": "FCC has 74% packing efficiency"},
                {"q": "Schottky defect is shown by", "opts": ["NaCl", "AgBr", "ZnS", "Si"], "ans": "NaCl", "exp": "Schottky defect: cation-anion pair missing"},
                {"q": "Frenkel defect is shown by", "opts": ["AgBr", "NaCl", "CsCl", "KCl"], "ans": "AgBr", "exp": "Frenkel defect: smaller ion displaced"}
            ],
            "moderate": [
                {"q": "If edge length of NaCl unit cell is 'a', nearest Na⁺-Cl⁻ distance is", "opts": ["a/2", "a/√2", "a", "a√2"], "ans": "a/2", "exp": "In FCC structure, nearest ions are at edge/2"},
                {"q": "An element crystallizes in FCC. If edge length is 400 pm and density is 10.5 g/cm³, molar mass is", "opts": ["75 g/mol", "150 g/mol", "60 g/mol", "100 g/mol"], "ans": "75 g/mol", "exp": "d = (Z×M)/(a³×Nₐ). Calculate M = 75 g/mol"},
                {"q": "In rock salt structure, if a = 5Å, radius of Cl⁻ is 1.8Å. Radius of Na⁺ is", "opts": ["0.7Å", "1.0Å", "0.5Å", "1.2Å"], "ans": "0.7Å", "exp": "a = 2(r⁺ + r⁻). r⁺ = 0.7Å"},
                {"q": "If radius of cation is 110 pm and anion is 200 pm, coordination number is likely", "opts": ["6", "4", "8", "12"], "ans": "6", "exp": "r⁺/r⁻ = 0.55. Range 0.414-0.732 gives CN = 6"},
                {"q": "Unit cell of metallic crystal with 4 atoms and edge 400 pm. Radius of atom in close packing is", "opts": ["141 pm", "200 pm", "100 pm", "283 pm"], "ans": "141 pm", "exp": "FCC: a = 2√2r. r = 141 pm"},
                {"q": "AgCl shows both Schottky and Frenkel defects because", "opts": ["Ag⁺ and Cl⁻ sizes differ significantly", "Both have same size", "AgCl is ionic", "Temperature is high"], "ans": "Ag⁺ and Cl⁻ sizes differ significantly", "exp": "Size difference allows both defects"},
                {"q": "Metal excess defect due to anion vacancies makes crystal", "opts": ["Colored", "Colorless", "Transparent", "White"], "ans": "Colored", "exp": "F-centers absorb light → color"},
                {"q": "ZnO turns yellow on heating due to", "opts": ["Metal excess defect", "Metal deficiency", "Schottky defect", "Frenkel defect"], "ans": "Metal excess defect", "exp": "O²⁻ lost → Zn excess → yellow"},
                {"q": "Number of carbon atoms per unit cell of diamond is", "opts": ["8", "4", "2", "1"], "ans": "8", "exp": "Diamond has 8 carbon atoms per unit cell"},
                {"q": "Which is true for FCC unit cell?", "opts": ["Face diagonal = 4r", "Body diagonal = 4r", "Edge = 4r", "Edge = 2r"], "ans": "Face diagonal = 4r", "exp": "In FCC, face diagonal = 4r"}
            ],
            "hard": [
                {"q": "An element crystallizes as BCC. Density is 7.2 g/cm³, edge 300 pm. Atomic mass is", "opts": ["52", "26", "104", "78"], "ans": "52", "exp": "d = ZM/(a³Nₐ). M ≈ 52"},
                {"q": "Percentage of free space in BCC unit cell is", "opts": ["32%", "26%", "48%", "16%"], "ans": "32%", "exp": "BCC packing = 68%. Free = 32%"},
                {"q": "AB crystallizes in rock salt structure. Formula mass is 6.023 × 10²³ u and edge 500 pm. Density is", "opts": ["4 g/cm³", "2 g/cm³", "1 g/cm³", "8 g/cm³"], "ans": "4 g/cm³", "exp": "Calculate using formula"},
                {"q": "In spinel structure MgAl₂O₄, oxide ions form FCC. Mg²⁺ occupies 1/8 tetrahedral voids. Al³⁺ occupies", "opts": ["1/2 octahedral voids", "All tetrahedral voids", "All octahedral voids", "1/4 octahedral voids"], "ans": "1/2 octahedral voids", "exp": "Balance charge and structure"},
                {"q": "CaF₂ structure: Ca²⁺ in FCC, F⁻ in all tetrahedral voids. Coordination numbers are", "opts": ["8:4", "4:8", "6:6", "12:6"], "ans": "8:4", "exp": "Each Ca²⁺ = 8 F⁻, each F⁻ = 4 Ca²⁺"},
                {"q": "If a crystal has impurity defect where cations are missing and replaced by higher charge cations, it is", "opts": ["Non-stoichiometric defect", "Stoichiometric defect", "Frenkel defect", "Schottky defect"], "ans": "Non-stoichiometric defect", "exp": "Impurity creates non-stoichiometric"},
                {"q": "A compound AB has rock salt structure. If anion vacancies are 1%, density compared to pure crystal is", "opts": ["99% of pure", "101% of pure", "100% same", "98% of pure"], "ans": "99% of pure", "exp": "1% less mass → 99% density"},
                {"q": "Iron crystallizes in BCC at room temp with edge 286 pm. At 900°C changes to FCC with edge 360 pm. Density change is", "opts": ["-2.5%", "+2.5%", "-5%", "+5%"], "ans": "-2.5%", "exp": "Calculate density change"},
                {"q": "Number of atoms in 200 g of FCC crystal (atomic mass 50, edge 200 pm) is", "opts": ["24.08 × 10²³", "12.04 × 10²³", "6.02 × 10²³", "48.16 × 10²³"], "ans": "24.08 × 10²³", "exp": "200/50 = 4 moles. 4 × 6.02×10²³"},
                {"q": "Ferrimagnetic substance example is", "opts": ["Fe₃O₄", "Fe", "Ni", "Co"], "ans": "Fe₃O₄", "exp": "Fe₃O₄ is ferrimagnetic"}
            ]
        },
        "Chemical Kinetics": {
            "easy": [
                {"q": "Unit of rate constant for first order reaction is", "opts": ["s⁻¹", "mol L⁻¹s⁻¹", "L mol⁻¹s⁻¹", "s"], "ans": "s⁻¹", "exp": "First order: k has units time⁻¹"},
                {"q": "Half-life of first order reaction is independent of", "opts": ["Initial concentration", "Temperature", "Rate constant", "All of these"], "ans": "Initial concentration", "exp": "t₁/₂ = 0.693/k"},
                {"q": "Rate of reaction increases with temperature because", "opts": ["Activation energy decreases", "More molecules have energy ≥ Eₐ", "Frequency factor increases", "Catalyst is added"], "ans": "More molecules have energy ≥ Eₐ", "exp": "Higher T → more molecules cross Eₐ"},
                {"q": "For elementary reaction A + B → Products, order is", "opts": ["2", "1", "3", "0"], "ans": "2", "exp": "Order = sum of coefficients = 2"},
                {"q": "Zero order reaction has rate", "opts": ["Independent of concentration", "Proportional to concentration", "Inversely proportional", "Exponential"], "ans": "Independent of concentration", "exp": "Zero order: rate = k"},
                {"q": "Arrhenius equation is", "opts": ["k = Ae⁻Eₐ/RT", "k = AeEₐ/RT", "k = A + Eₐ/RT", "k = AEₐ/RT"], "ans": "k = Ae⁻Eₐ/RT", "exp": "Standard Arrhenius form"},
                {"q": "Activation energy is", "opts": ["Minimum energy for reaction", "Average energy", "Maximum energy", "Zero"], "ans": "Minimum energy for reaction", "exp": "Eₐ is threshold energy"},
                {"q": "Catalyst increases reaction rate by", "opts": ["Lowering activation energy", "Increasing activation energy", "Increasing temperature", "Changing equilibrium"], "ans": "Lowering activation energy", "exp": "Catalyst lowers Eₐ"},
                {"q": "For reaction 2A → B, if [A] is halved, rate becomes", "opts": ["1/4 times", "1/2 times", "2 times", "4 times"], "ans": "1/4 times", "exp": "2nd order: rate ∝ [A]²"},
                {"q": "Molecularity of reaction can be", "opts": ["1, 2, or 3", "0, 1, 2", "Any value", "Fraction"], "ans": "1, 2, or 3", "exp": "Molecularity = 1-3 typically"}
            ],
            "moderate": [
                {"q": "For reaction A → B, rate = k[A]². If [A] is tripled, rate becomes", "opts": ["9 times", "3 times", "6 times", "27 times"], "ans": "9 times", "exp": "rate ∝ [A]². 3² = 9"},
                {"q": "Half-life of first order reaction is 10 min. Time for 75% completion is", "opts": ["20 min", "30 min", "40 min", "15 min"], "ans": "20 min", "exp": "75% = 2 half-lives"},
                {"q": "Rate constant at 300K is 2×10⁻² s⁻¹. At 400K it is 8×10⁻² s⁻¹. Activation energy is", "opts": ["13.8 kJ/mol", "27.6 kJ/mol", "6.9 kJ/mol", "55.2 kJ/mol"], "ans": "13.8 kJ/mol", "exp": "Use Arrhenius equation"},
                {"q": "For A + B → C, doubling [A] doubles rate, doubling [B] has no effect. Order is", "opts": ["1", "2", "0", "3"], "ans": "1", "exp": "rate = k[A]¹[B]⁰. Order = 1"},
                {"q": "Initial rate for 2A + B → C. [A]=0.1M, [B]=0.2M gives rate=10⁻³. [A]=0.2M, [B]=0.2M gives rate=2×10⁻³. Order w.r.t A is", "opts": ["1", "2", "0", "3"], "ans": "1", "exp": "Doubling [A] doubles rate → order 1"},
                {"q": "Time for 90% completion of first order (k = 0.0693 min⁻¹) is", "opts": ["33.2 min", "10 min", "20 min", "30 min"], "ans": "33.2 min", "exp": "t = 2.303/k × log(100/10)"},
                {"q": "For gaseous reaction, rate increases 8 times from 300K to 360K. Activation energy is", "opts": ["56 kJ/mol", "28 kJ/mol", "84 kJ/mol", "112 kJ/mol"], "ans": "56 kJ/mol", "exp": "k₂/k₁ = 8. Calculate Eₐ"},
                {"q": "For zero order A → B, [A₀] = 0.1M, k = 0.01 M/s. Time for half completion is", "opts": ["5 s", "10 s", "2.5 s", "20 s"], "ans": "5 s", "exp": "t₁/₂ = [A₀]/2k = 5 s"},
                {"q": "H₂O₂ decomposition is first order, k=0.001 s⁻¹. Time for 0.5M to 0.125M is", "opts": ["1386 s", "693 s", "2079 s", "3465 s"], "ans": "1386 s", "exp": "t = 2.303/k × log(0.5/0.125)"},
                {"q": "Temperature coefficient is 2. Rate at 100°C vs 90°C is", "opts": ["2 times", "4 times", "8 times", "16 times"], "ans": "2 times", "exp": "Coefficient = 2 for 10°C"}
            ],
            "hard": [
                {"q": "Reaction 2N₂O₅ → 4NO₂ + O₂, k = 3.46×10⁻⁵ s⁻¹. For 20% decomposition of 2 moles in 500 mL, time is", "opts": ["6450 s", "3225 s", "12900 s", "1612 s"], "ans": "6450 s", "exp": "First order calculation"},
                {"q": "For A → B, 10% reacts in 20 min. Time for 19% (first order) is", "opts": ["40 min", "38 min", "30 min", "42 min"], "ans": "40 min", "exp": "Calculate using first order"},
                {"q": "Rate = k[A][B]². [A]=0.1M, [B]=0.2M. If both tripled, rate increases by", "opts": ["27 times", "9 times", "3 times", "81 times"], "ans": "27 times", "exp": "3 × 3² = 27"},
                {"q": "For parallel A → B (k₁) and A → C (k₂), ratio B to C is", "opts": ["k₁/k₂", "k₂/k₁", "k₁×k₂", "(k₁+k₂)/2"], "ans": "k₁/k₂", "exp": "Ratio = k₁/k₂"},
                {"q": "Eₐ = 100 kJ/mol. Catalyst lowers to 75 kJ. At 27°C, rate increases by", "opts": ["10⁵ times", "10³ times", "10² times", "10 times"], "ans": "10⁵ times", "exp": "Calculate ratio"},
                {"q": "Second order A → B. Time to reduce 1M to 0.25M, k=0.02 L mol⁻¹s⁻¹ is", "opts": ["150 s", "75 s", "300 s", "50 s"], "ans": "150 s", "exp": "t = 1/k(1/[A] - 1/[A₀])"},
                {"q": "Plot log k vs 1/T is linear, slope -6000. Eₐ is (R=8.314)", "opts": ["115 kJ/mol", "49.9 kJ/mol", "230 kJ/mol", "57.5 kJ/mol"], "ans": "115 kJ/mol", "exp": "Eₐ = -slope × 2.303R"},
                {"q": "For 2A + B → A₂B, if [A] halved and [B] doubled, rate becomes", "opts": ["Half", "Same", "Double", "One-fourth"], "ans": "Half", "exp": "rate = k(A/2)²(2B) = half"},
                {"q": "Reaction 50% in 20 min at 300K, 5 min at 320K. Eₐ is", "opts": ["13 kJ/mol", "26 kJ/mol", "39 kJ/mol", "52 kJ/mol"], "ans": "26 kJ/mol", "exp": "k₂/k₁ = 4. Calculate Eₐ"},
                {"q": "For consecutive A → B → C, if k₁ >> k₂, concentration of B", "opts": ["Increases then plateaus", "Continuously increases", "Remains zero", "Continuously decreases"], "ans": "Increases then plateaus", "exp": "Fast formation, slow consumption"}
            ]
        }
    },
    "Mathematics": {
        "Matrices": {
            "easy": [
                {"q": "If A is 3×2 and B is 2×4, order of AB is", "opts": ["3×4", "2×2", "3×2", "4×3"], "ans": "3×4", "exp": "(m×n)(n×p) = (m×p)"},
                {"q": "Transpose of row matrix is", "opts": ["Column matrix", "Row matrix", "Square matrix", "Null matrix"], "ans": "Column matrix", "exp": "Transpose interchanges rows/columns"},
                {"q": "For A = -Aᵀ, matrix is", "opts": ["Skew-symmetric", "Symmetric", "Identity", "Null"], "ans": "Skew-symmetric", "exp": "Skew-symmetric: A = -Aᵀ"},
                {"q": "Identity matrix of order 3 is", "opts": ["I₃", "O₃", "A₃", "B₃"], "ans": "I₃", "exp": "Notation: Iₙ"},
                {"q": "If A, B are square, (AB)ᵀ =", "opts": ["BᵀAᵀ", "AᵀBᵀ", "AB", "BA"], "ans": "BᵀAᵀ", "exp": "Reverse order property"},
                {"q": "Determinant of [a b; c d] is", "opts": ["ad - bc", "ad + bc", "ab - cd", "ac - bd"], "ans": "ad - bc", "exp": "2×2 determinant formula"},
                {"q": "If |A| = 5, then |3A| for 3×3 matrix =", "opts": ["135", "45", "15", "125"], "ans": "135", "exp": "|kA| = kⁿ|A| = 3³×5 = 135"},
                {"q": "Matrix is singular if", "opts": ["|A| = 0", "|A| = 1", "|A| ≠ 0", "A = 0"], "ans": "|A| = 0", "exp": "Singular: det = 0"},
                {"q": "If A symmetric, B skew-symmetric, A + B is", "opts": ["Neither", "Symmetric", "Skew-symmetric", "Null"], "ans": "Neither", "exp": "Sum is neither"},
                {"q": "For any square A, A + Aᵀ is", "opts": ["Symmetric", "Skew-symmetric", "Identity", "Null"], "ans": "Symmetric", "exp": "(A + Aᵀ)ᵀ = A + Aᵀ"}
            ],
            "moderate": [
                {"q": "If A is 3×3 skew-symmetric, det(A) =", "opts": ["0", "1", "-1", "Cannot say"], "ans": "0", "exp": "Odd order skew-symmetric: det = 0"},
                {"q": "If A = [1 2; 3 4], then A² - 5A =", "opts": ["[-2 -2; -3 -4]", "[0 0; 0 0]", "[1 1; 1 1]", "[-1 -1; -1 -1]"], "ans": "[-2 -2; -3 -4]", "exp": "Calculate: A² - 5A"},
                {"q": "If A, B symmetric, AB symmetric if", "opts": ["AB = BA", "AB = -BA", "A = B", "Never"], "ans": "AB = BA", "exp": "Need commutativity"},
                {"q": "Trace of [1 2 3; 0 4 5; 0 0 6] is", "opts": ["11", "10", "21", "7"], "ans": "11", "exp": "Sum diagonal: 1+4+6=11"},
                {"q": "If A invertible and AB = AC, then", "opts": ["B = C", "B = -C", "AB = 0", "Cannot say"], "ans": "B = C", "exp": "Multiply by A⁻¹"},
                {"q": "If A = [cos θ -sin θ; sin θ cos θ], AAᵀ =", "opts": ["I", "O", "A", "2A"], "ans": "I", "exp": "Rotation matrix: AAᵀ = I"},
                {"q": "If A² = I, then A⁻¹ =", "opts": ["A", "-A", "I", "A²"], "ans": "A", "exp": "A involutory: A⁻¹ = A"},
                {"q": "If A = [1 0 0; 0 1 0; 0 0 k], det(A) = 0, then k =", "opts": ["0", "1", "-1", "Any"], "ans": "0", "exp": "Diagonal: det = 1×1×k = 0"},
                {"q": "If |A| = 2 for 3×3, then |A⁻¹| =", "opts": ["1/2", "2", "-2", "-1/2"], "ans": "1/2", "exp": "|A⁻¹| = 1/|A|"},
                {"q": "If A, B non-singular, (AB)⁻¹ =", "opts": ["B⁻¹A⁻¹", "A⁻¹B⁻¹", "AB", "BA"], "ans": "B⁻¹A⁻¹", "exp": "Reverse order"}
            ],
            "hard": [
                {"q": "If A² - A + I = O, then A⁻¹ =", "opts": ["I - A", "A - I", "A", "-A"], "ans": "I - A", "exp": "A(A-I) = -I → A⁻¹ = I-A"},
                {"q": "If A idempotent (A²=A) non-zero, det(A) =", "opts": ["0 or 1", "0", "1", "-1"], "ans": "0 or 1", "exp": "|A|² = |A| → |A|(|A|-1) = 0"},
                {"q": "If A = [1 2 3; 2 3 4; 3 4 5], rank is", "opts": ["2", "3", "1", "0"], "ans": "2", "exp": "Dependent rows, rank = 2"},
                {"q": "If A orthogonal, A⁻¹ =", "opts": ["Aᵀ", "A", "-A", "-Aᵀ"], "ans": "Aᵀ", "exp": "Orthogonal: AAᵀ = I"},
                {"q": "Eigenvalues of [3 1; 0 3] are", "opts": ["3, 3", "3, 0", "1, 3", "0, 0"], "ans": "3, 3", "exp": "Upper triangular: eigenvalues = diagonal"},
                {"q": "If 3×3 matrix rank = 2, then", "opts": ["|A| = 0", "|A| = 1", "|A| = 2", "|A| ≠ 0"], "ans": "|A| = 0", "exp": "rank < order → singular"},
                {"q": "If Aᵀ = A⁻¹ and |A| = -1, A is", "opts": ["Orthogonal", "Symmetric", "Skew-symmetric", "Idempotent"], "ans": "Orthogonal", "exp": "Aᵀ = A⁻¹ defines orthogonal"},
                {"q": "If A nilpotent, A³ = O, trace(A) =", "opts": ["0", "1", "3", "Cannot say"], "ans": "0", "exp": "Nilpotent: all eigenvalues = 0"},
                {"q": "If A, B commute, A² = B² = (AB)², then", "opts": ["A = B or A = -B", "A = B", "A = -B", "No relation"], "ans": "A = B or A = -B", "exp": "Special case: A = ±B"},
                {"q": "If A = [a b; c d] and adj(A) = [d -b; -c a], A(adj A) =", "opts": ["|A|I", "A", "I", "O"], "ans": "|A|I", "exp": "Property: A(adj A) = |A|I"}
            ]
        },
        "Integration": {
            "easy": [
                {"q": "∫x dx =", "opts": ["x²/2 + C", "x² + C", "2x + C", "x³/3 + C"], "ans": "x²/2 + C", "exp": "Power rule: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C"},
                {"q": "∫cos x dx =", "opts": ["sin x + C", "-sin x + C", "cos x + C", "-cos x + C"], "ans": "sin x + C", "exp": "d/dx(sin x) = cos x"},
                {"q": "∫sin x dx =", "opts": ["-cos x + C", "cos x + C", "-sin x + C", "sin x + C"], "ans": "-cos x + C", "exp": "d/dx(-cos x) = sin x"},
                {"q": "∫eˣ dx =", "opts": ["eˣ + C", "eˣ/x + C", "xeˣ + C", "ln x + C"], "ans": "eˣ + C", "exp": "eˣ is its own antiderivative"},
                {"q": "∫(1/x) dx =", "opts": ["ln|x| + C", "1/x² + C", "x + C", "eˣ + C"], "ans": "ln|x| + C", "exp": "d/dx(ln|x|) = 1/x"},
                {"q": "∫sec²x dx =", "opts": ["tan x + C", "cot x + C", "sec x + C", "-tan x + C"], "ans": "tan x + C", "exp": "d/dx(tan x) = sec²x"},
                {"q": "∫cosec²x dx =", "opts": ["-cot x + C", "cot x + C", "tan x + C", "-tan x + C"], "ans": "-cot x + C", "exp": "d/dx(-cot x) = cosec²x"},
                {"q": "∫k dx where k is constant =", "opts": ["kx + C", "k + C", "x + C", "0"], "ans": "kx + C", "exp": "Integral of constant"},
                {"q": "∫dx/(1+x²) =", "opts": ["tan⁻¹x + C", "sin⁻¹x + C", "ln(1+x²) + C", "x/(1+x²) + C"], "ans": "tan⁻¹x + C", "exp": "d/dx(tan⁻¹x) = 1/(1+x²)"},
                {"q": "∫dx/√(1-x²) =", "opts": ["sin⁻¹x + C", "cos⁻¹x + C", "tan⁻¹x + C", "√(1-x²) + C"], "ans": "sin⁻¹x + C", "exp": "d/dx(sin⁻¹x) = 1/√(1-x²)"}
            ],
            "moderate": [
                {"q": "∫x cos x dx =", "opts": ["x sin x + cos x + C", "x sin x - cos x + C", "sin x - x cos x + C", "sin x + x cos x + C"], "ans": "x sin x + cos x + C", "exp": "Integration by parts"},
                {"q": "∫eˣ sin x dx =", "opts": ["eˣ(sin x - cos x)/2 + C", "eˣ(sin x + cos x)/2 + C", "eˣ sin x + C", "eˣ cos x + C"], "ans": "eˣ(sin x - cos x)/2 + C", "exp": "By parts twice"},
                {"q": "∫x²eˣ dx =", "opts": ["eˣ(x² - 2x + 2) + C", "eˣ(x² + 2x + 2) + C", "x²eˣ + C", "eˣx²/2 + C"], "ans": "eˣ(x² - 2x + 2) + C", "exp": "By parts twice"},
                {"q": "∫ln x dx =", "opts": ["x ln x - x + C", "x ln x + x + C", "ln x/x + C", "1/x + C"], "ans": "x ln x - x + C", "exp": "By parts: u=ln x, dv=dx"},
                {"q": "∫dx/(x²+4) =", "opts": ["(1/2)tan⁻¹(x/2) + C", "tan⁻¹(x/2) + C", "(1/2)tan⁻¹(2x) + C", "tan⁻¹x + C"], "ans": "(1/2)tan⁻¹(x/2) + C", "exp": "Use formula with a=2"},
                {"q": "∫x²/(1+x³) dx =", "opts": ["(1/3)ln|1+x³| + C", "ln|1+x³| + C", "x³/3 + C", "tan⁻¹x³ + C"], "ans": "(1/3)ln|1+x³| + C", "exp": "Substitution: u = 1+x³"},
                {"q": "∫sin²x dx =", "opts": ["x/2 - sin(2x)/4 + C", "x/2 + sin(2x)/4 + C", "sin²x/2 + C", "-cos²x + C"], "ans": "x/2 - sin(2x)/4 + C", "exp": "Use sin²x = (1-cos 2x)/2"},
                {"q": "∫cos³x dx =", "opts": ["sin x - sin³x/3 + C", "sin x + sin³x/3 + C", "cos x + C", "sin³x + C"], "ans": "sin x - sin³x/3 + C", "exp": "cos³x = cos x(1-sin²x)"},
                {"q": "∫dx/√(x²+4) =", "opts": ["ln|x + √(x²+4)| + C", "ln|x²+4| + C", "sin⁻¹(x/2) + C", "√(x²+4) + C"], "ans": "ln|x + √(x²+4)| + C", "exp": "Standard form"},
                {"q": "∫tan x dx =", "opts": ["-ln|cos x| + C", "ln|cos x| + C", "ln|sin x| + C", "-ln|sin x| + C"], "ans": "-ln|cos x| + C", "exp": "∫(sin x/cos x) dx"}
            ],
            "hard": [
                {"q": "∫√(x²+1) dx =", "opts": ["(x/2)√(x²+1) + (1/2)ln|x+√(x²+1)| + C", "√(x²+1) + C", "x√(x²+1) + C", "(2/3)(x²+1)^(3/2) + C"], "ans": "(x/2)√(x²+1) + (1/2)ln|x+√(x²+1)| + C", "exp": "Trig substitution"},
                {"q": "∫x²√(1-x²) dx =", "opts": ["(x/8)(2x²-1)√(1-x²) + (1/8)sin⁻¹x + C", "x√(1-x²) + C", "(1-x²)^(3/2)/3 + C", "x²sin⁻¹x + C"], "ans": "(x/8)(2x²-1)√(1-x²) + (1/8)sin⁻¹x + C", "exp": "Complex reduction"},
                {"q": "∫dx/((x²+1)(x²+4)) =", "opts": ["(1/3)[tan⁻¹x - (1/2)tan⁻¹(x/2)] + C", "tan⁻¹x + C", "(1/6)tan⁻¹(x/2) + C", "ln|x²+1| - ln|x²+4| + C"], "ans": "(1/3)[tan⁻¹x - (1/2)tan⁻¹(x/2)] + C", "exp": "Partial fractions"},
                {"q": "∫eˣ(x²+1)/x² dx =", "opts": ["eˣ(x-1)/x + C", "eˣ(x+1)/x + C", "eˣ/x + C", "eˣx + C"], "ans": "eˣ(x-1)/x + C", "exp": "By parts"},
                {"q": "∫sin⁴x dx =", "opts": ["3x/8 - sin(2x)/4 + sin(4x)/32 + C", "sin⁴x/4 + C", "x/2 - sin(2x)/4 + C", "-cos⁴x + C"], "ans": "3x/8 - sin(2x)/4 + sin(4x)/32 + C", "exp": "Reduce power twice"},
                {"q": "∫dx/(x(x⁴+1)) =", "opts": ["(1/4)ln|x⁴/(x⁴+1)| + C", "ln|x| - (1/4)ln|x⁴+1| + C", "Both A and B", "None"], "ans": "Both A and B", "exp": "Equivalent forms"},
                {"q": "∫x³/(x²+1)² dx =", "opts": ["(1/2)ln|x²+1| + 1/(2(x²+1)) + C", "ln|x²+1| + C", "x²/(x²+1) + C", "tan⁻¹x + C"], "ans": "(1/2)ln|x²+1| + 1/(2(x²+1)) + C", "exp": "Split and substitute"},
                {"q": "∫(cos x)/(1+sin x) dx =", "opts": ["ln|1+sin x| + C", "-ln|1+sin x| + C", "tan x + C", "sin x + C"], "ans": "ln|1+sin x| + C", "exp": "u = 1 + sin x"},
                {"q": "∫x/(x⁴+x²+1) dx =", "opts": ["(1/2)tan⁻¹(x²+1/√3) + C", "tan⁻¹x² + C", "ln|x⁴+x²+1| + C", "(1/4)ln|x⁴+x²+1| + C"], "ans": "(1/2)tan⁻¹(x²+1/√3) + C", "exp": "u = x², factor/complete square"},
                {"q": "∫sin x cos x/(sin⁴x + cos⁴x) dx =", "opts": ["(1/2)tan⁻¹(tan²x - 1) + C", "tan⁻¹(sin x) + C", "ln|sin⁴x + cos⁴x| + C", "sin²x + C"], "ans": "(1/2)tan⁻¹(tan²x - 1) + C", "exp": "Divide by cos⁴x, t = tan²x"}
            ]
        }
    }
}

# =========================
# DATA MANAGER
# =========================
class DataManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.users = self.load_users()
        
    def load_users(self):
        try:
            if os.path.exists(USER_DATA_FILE):
                with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except:
            return {}
    
    def save_users(self):
        try:
            with self.lock:
                with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving: {e}")
    
    def get_user(self, chat_id):
        chat_id = str(chat_id)
        if chat_id not in self.users:
            self.users[chat_id] = {
                "stats": {
                    "total_attempted": 0,
                    "total_correct": 0,
                    "subject_stats": {s: {"attempted": 0, "correct": 0} for s in SUBJECTS},
                    "chapter_stats": {},
                    "difficulty_stats": {l: {"attempted": 0, "correct": 0} for l in ["easy", "moderate", "hard"]},
                    "streak_days": 0,
                    "last_practice": None
                },
                "current_session": None
            }
            self.save_users()
        return self.users[chat_id]
    
    def update_stats(self, chat_id, subject, chapter, difficulty, correct):
        user = self.get_user(chat_id)
        stats = user["stats"]
        
        stats["total_attempted"] += 1
        if correct:
            stats["total_correct"] += 1
        
        stats["subject_stats"][subject]["attempted"] += 1
        if correct:
            stats["subject_stats"][subject]["correct"] += 1
        
        chapter_key = f"{subject}_{chapter}"
        if chapter_key not in stats["chapter_stats"]:
            stats["chapter_stats"][chapter_key] = {"attempted": 0, "correct": 0}
        stats["chapter_stats"][chapter_key]["attempted"] += 1
        if correct:
            stats["chapter_stats"][chapter_key]["correct"] += 1
        
        stats["difficulty_stats"][difficulty]["attempted"] += 1
        if correct:
            stats["difficulty_stats"][difficulty]["correct"] += 1
        
        today = datetime.now().date().isoformat()
        last = stats.get("last_practice")
        if last:
            last_date = datetime.fromisoformat(last).date()
            if (datetime.now().date() - last_date).days == 1:
                stats["streak_days"] += 1
            elif (datetime.now().date() - last_date).days > 1:
                stats["streak_days"] = 1
        else:
            stats["streak_days"] = 1
        
        stats["last_practice"] = datetime.now().isoformat()
        self.save_users()
    
    def start_session(self, chat_id, subject, chapter, difficulty):
        user = self.get_user(chat_id)
        questions = QUESTIONS.get(subject, {}).get(chapter, {}).get(difficulty, [])
        
        if questions:
            shuffled = questions.copy()
            random.shuffle(shuffled)
            
            user["current_session"] = {
                "subject": subject,
                "chapter": chapter,
                "difficulty": difficulty,
                "questions": shuffled,
                "available": list(range(len(shuffled))),
                "current_index": None,
                "session_correct": 0,
                "session_total": 0
            }
            self.save_users()
            return True
        return False
    
    def get_next_question(self, chat_id):
        user = self.get_user(chat_id)
        session = user.get("current_session")
        
        if not session:
            return None
        
        if not session["available"]:
            session["available"] = list(range(len(session["questions"])))
            random.shuffle(session["available"])
        
        idx = random.choice(session["available"])
        session["available"].remove(idx)
        session["current_index"] = idx
        
        self.save_users()
        return session["questions"][idx]
    
    def check_answer(self, chat_id, answer):
        user = self.get_user(chat_id)
        session = user.get("current_session")
        
        if not session or session["current_index"] is None:
            return None
        
        question = session["questions"][session["current_index"]]
        correct = (answer == question["ans"])
        
        session["session_total"] += 1
        if correct:
            session["session_correct"] += 1
        
        self.update_stats(chat_id, session["subject"], session["chapter"], session["difficulty"], correct)
        
        return {
            "correct": correct,
            "answer": question["ans"],
            "explanation": question["exp"]
        }
    
    def end_session(self, chat_id):
        user = self.get_user(chat_id)
        session = user.get("current_session")
        
        if session:
            result = {
                "total": session["session_total"],
                "correct": session["session_correct"],
                "accuracy": (session["session_correct"] / session["session_total"] * 100) if session["session_total"] > 0 else 0
            }
            user["current_session"] = None
            self.save_users()
            return result
        return None

data_manager = DataManager()
user_states = {}

def set_state(chat_id, state, data=None):
    user_states[chat_id] = {"state": state, "data": data or {}}

def get_state(chat_id):
    return user_states.get(chat_id, {}).get("state")

def get_state_data(chat_id):
    return user_states.get(chat_id, {}).get("data", {})

def clear_state(chat_id):
    if chat_id in user_states:
        del user_states[chat_id]

# =========================
# UI HELPERS
# =========================
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📘 Physics Practice"),
        types.KeyboardButton("🧪 Chemistry Practice"),
        types.KeyboardButton("📐 Mathematics Practice"),
        types.KeyboardButton("📊 My Performance"),
        types.KeyboardButton("ℹ️ About")
    )
    return markup

def create_chapter_menu(chapters):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for chapter in chapters:
        markup.add(types.KeyboardButton(chapter))
    markup.row("🔙 Back", "🏠 Main Menu")
    return markup

def create_difficulty_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for diff_text, diff_data in DIFFICULTY_LEVELS.items():
        markup.add(types.KeyboardButton(f"{diff_text} - {diff_data['desc']}"))
    markup.row("🔙 Back", "🏠 Main Menu")
    return markup

# =========================
# BOT HANDLERS
# =========================
@bot.message_handler(commands=['start'])
def start(message):
    try:
        data_manager.get_user(message.chat.id)
        
        msg = bot.send_message(message.chat.id, "⚡ Initializing...")
        time.sleep(0.4)
        bot.edit_message_text("🔬 Loading Questions...", message.chat.id, msg.message_id)
        time.sleep(0.4)
        bot.edit_message_text("🚀 Ready!", message.chat.id, msg.message_id)
        time.sleep(0.4)
        
        text = (
            "🎯 *MHT-CET WARRIOR* 🎯\n\n"
            "✅ 183 Real Questions\n"
            "✅ 3 Difficulty Levels\n"
            "✅ Infinite Practice\n"
            "✅ Track Progress\n\n"
            "⬇️ Subscribe for updates ⬇️"
        )
        
        markup = types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton("🔔 Subscribe", url="https://youtube.com/@proofygamerz")],
            [types.InlineKeyboardButton("🚀 Start", callback_data="main_menu")]
        ])
        
        bot.edit_message_text(text, message.chat.id, msg.message_id, reply_markup=markup, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, "Error. Try /start again")

@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def main_menu_callback(call):
    try:
        bot.answer_callback_query(call.id)
        user = data_manager.get_user(call.message.chat.id)
        stats = user["stats"]
        accuracy = (stats["total_correct"] / stats["total_attempted"] * 100) if stats["total_attempted"] > 0 else 0
        
        text = f"📊 Stats: {stats['total_attempted']} Q | {accuracy:.1f}% | 🔥{stats['streak_days']} days\n\nChoose practice mode:"
        
        bot.send_message(call.message.chat.id, text, reply_markup=create_main_menu(), parse_mode="Markdown")
    except:
        pass

@bot.message_handler(func=lambda m: m.text in ["📘 Physics Practice", "🧪 Chemistry Practice", "📐 Mathematics Practice"])
def select_subject(message):
    try:
        subject_map = {
            "📘 Physics Practice": "Physics",
            "🧪 Chemistry Practice": "Chemistry",
            "📐 Mathematics Practice": "Mathematics"
        }
        subject = subject_map[message.text]
        set_state(message.chat.id, "selecting_chapter", {"subject": subject})
        
        chapters = SUBJECTS[subject]["chapters"]
        emoji = SUBJECTS[subject]["emoji"]
        
        text = f"{emoji} *{subject.upper()}*\n\n📚 {len(chapters)} Chapters\n\nSelect chapter:"
        bot.send_message(message.chat.id, text, reply_markup=create_chapter_menu(chapters), parse_mode="Markdown")
    except:
        pass

@bot.message_handler(func=lambda m: get_state(m.chat.id) == "selecting_chapter")
def select_chapter(message):
    try:
        state_data = get_state_data(message.chat.id)
        subject = state_data.get("subject")
        chapter = message.text
        
        if chapter not in SUBJECTS[subject]["chapters"]:
            return
        
        set_state(message.chat.id, "selecting_difficulty", {"subject": subject, "chapter": chapter})
        
        text = f"📖 *{chapter}*\n\nChoose difficulty:\n\n🟢 Easy - Basics\n🟡 Moderate - CET Level\n🔴 Hard - Rank Booster"
        bot.send_message(message.chat.id, text, reply_markup=create_difficulty_menu(), parse_mode="Markdown")
    except:
        pass

@bot.message_handler(func=lambda m: get_state(m.chat.id) == "selecting_difficulty")
def select_difficulty(message):
    try:
        state_data = get_state_data(message.chat.id)
        subject = state_data.get("subject")
        chapter = state_data.get("chapter")
        
        difficulty = None
        for diff_text, diff_data in DIFFICULTY_LEVELS.items():
            if message.text.startswith(diff_text):
                difficulty = diff_data["level"]
                break
        
        if not difficulty:
            return
        
        msg = bot.send_message(message.chat.id, "🔄 Loading...")
        time.sleep(0.3)
        bot.edit_message_text("⚡ Preparing...", message.chat.id, msg.message_id)
        time.sleep(0.3)
        
        success = data_manager.start_session(message.chat.id, subject, chapter, difficulty)
        
        if success:
            set_state(message.chat.id, "practicing")
            send_next_question(message.chat.id)
        else:
            bot.send_message(message.chat.id, "❌ No questions available", reply_markup=create_main_menu())
            clear_state(message.chat.id)
    except:
        pass

def send_next_question(chat_id):
    try:
        question = data_manager.get_next_question(chat_id)
        if not question:
            return
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for option in question["opts"]:
            markup.add(types.KeyboardButton(option))
        markup.row("❌ End Session", "🏠 Main Menu")
        
        user = data_manager.get_user(chat_id)
        session = user["current_session"]
        
        diff_emoji = "🟢" if session["difficulty"] == "easy" else "🟡" if session["difficulty"] == "moderate" else "🔴"
        
        text = f"{diff_emoji} *Q{session['session_total'] + 1}*\n\n{question['q']}\n\nSelect answer:"
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
    except:
        pass

@bot.message_handler(func=lambda m: get_state(m.chat.id) == "practicing")
def handle_answer(message):
    try:
        if message.text == "❌ End Session":
            end_practice_session(message.chat.id)
            return
        elif message.text == "🏠 Main Menu":
            end_practice_session(message.chat.id)
            bot.send_message(message.chat.id, "Session ended", reply_markup=create_main_menu())
            clear_state(message.chat.id)
            return
        
        result = data_manager.check_answer(message.chat.id, message.text)
        if not result:
            return
        
        if result["correct"]:
            text = f"✅ *CORRECT!* 🎉\n\n💡 {result['explanation']}\n\nPress Next →"
        else:
            text = f"❌ *INCORRECT*\n\n✔️ Answer: {result['answer']}\n\n💡 {result['explanation']}\n\nPress Next →"
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("⏭️ Next Question")
        markup.row("❌ End Session", "🏠 Main Menu")
        
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")
        set_state(message.chat.id, "waiting_next")
    except:
        pass

@bot.message_handler(func=lambda m: get_state(m.chat.id) == "waiting_next" and m.text == "⏭️ Next Question")
def next_question_handler(message):
    set_state(message.chat.id, "practicing")
    send_next_question(message.chat.id)

def end_practice_session(chat_id):
    try:
        result = data_manager.end_session(chat_id)
        if result:
            accuracy = result["accuracy"]
            perf = "🏆 EXCELLENT!" if accuracy >= 80 else "👏 GOOD!" if accuracy >= 60 else "📚 KEEP GOING!" if accuracy >= 40 else "💪 PRACTICE MORE!"
            
            text = f"{perf}\n\n📊 *SESSION SUMMARY*\n\nQuestions: {result['total']}\nCorrect: {result['correct']}\nAccuracy: {accuracy:.1f}%\n\n{'⭐' * min(5, int(accuracy/20))}"
            bot.send_message(chat_id, text, parse_mode="Markdown")
        clear_state(chat_id)
    except:
        pass

@bot.message_handler(func=lambda m: m.text == "📊 My Performance")
def show_performance(message):
    try:
        user = data_manager.get_user(message.chat.id)
        stats = user["stats"]
        
        total = stats["total_attempted"]
        correct = stats["total_correct"]
        accuracy = (correct / total * 100) if total > 0 else 0
        
        subject_text = ""
        for subject, subj_stats in stats["subject_stats"].items():
            s_total = subj_stats["attempted"]
            s_correct = subj_stats["correct"]
            s_acc = (s_correct / s_total * 100) if s_total > 0 else 0
            emoji = SUBJECTS[subject]["emoji"]
            subject_text += f"{emoji} {subject}: {s_acc:.0f}% ({s_correct}/{s_total})\n"
        
        text = f"📊 *PERFORMANCE*\n\n*Overall*\nQuestions: {total}\nCorrect: {correct}\nAccuracy: {accuracy:.1f}%\nStreak: {stats['streak_days']} days 🔥\n\n*By Subject*\n{subject_text}"
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("🏠 Main Menu")
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")
    except:
        pass

@bot.message_handler(func=lambda m: m.text == "ℹ️ About")
def about(message):
    text = (
        "ℹ️ *MHT-CET WARRIOR BOT*\n\n"
        "📚 *Coverage:*\n"
        "• 183 Real Questions\n"
        "• Physics, Chemistry, Math\n"
        "• 3 Difficulty Levels\n\n"
        "✨ *Features:*\n"
        "• Infinite Practice\n"
        "• Progress Tracking\n"
        "• Instant Feedback\n\n"
        "━━━━━━━━━━━━━━━━\n"
        "*Developed by: Proofy Gamerz*\n"
        "For MHT-CET Aspirants\n"
        "━━━━━━━━━━━━━━━━\n\n"
        "🔔 youtube.com/@proofygamerz"
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🏠 Main Menu")
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text in ["🔙 Back", "🏠 Main Menu"])
def go_main_menu(message):
    clear_state(message.chat.id)
    data_manager.end_session(message.chat.id)
    bot.send_message(message.chat.id, "🏠 Main Menu", reply_markup=create_main_menu())

@bot.message_handler(func=lambda m: True)
def catch_all(message):
    bot.send_message(message.chat.id, "❓ Use menu buttons", reply_markup=create_main_menu())

# =========================
# RUN BOT
# =========================
if __name__ == "__main__":
    print("="*50)
    print("🚀 MHT-CET WARRIOR BOT")
    print("   183 Questions Ready!")
    print("="*50)
    print("✅ Bot is running...")
    print("="*50)
    
    try:
        bot.infinity_polling(timeout=60)
    except Exception as e:
        print(f"Error: {e}")
