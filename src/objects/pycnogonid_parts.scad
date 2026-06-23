// ==============================================================================
// 🤖 ARTICULATED ROBOT COMPONENT GENERATOR
// ==============================================================================
$fn = 32;

// Choose which specific part to render for export:
// "TRUNK_SEGMENT", "PROBOSCIS", "COXA", "FEMUR", "TIBIA"
part_type = "FEMUR"; 

// Dimensions
radius = 1.0;
length_femur = 10.0;
length_tibia = 9.0;
length_coxa = 2.5;

module joint_socket() {
    // Spherical indentation to represent a physical mechanical joint pivot
    sphere(r = radius * 1.3);
}

module joint_ball(len) {
    // Ball hinge tip at the distal end of the limb segment
    translate([0, 0, len])
        sphere(r = radius * 1.1);
}

// Render Engine Logic
if (part_type == "TRUNK_SEGMENT") {
    difference() {
        union() {
            cylinder(h = 4.0, r = 2.0, center = true);
            // Left & Right Lateral Hinge Extenders
            rotate([0, 90, 0]) cylinder(h = 6.0, r = 1.2, center = true);
        }
        // Hollow sockets out the sides for the Coxa joints
        translate([3.0, 0, 0]) joint_socket();
        translate([-3.0, 0, 0]) joint_socket();
    }
}

if (part_type == "PROBOSCIS") {
    union() {
        cylinder(h = 7.0, r1 = 1.8, r2 = 1.2, center = false);
        joint_ball(7.0);
    }
}

if (part_type == "COXA") {
    difference() {
        union() {
            cylinder(h = length_coxa, r = radius * 1.3);
            joint_ball(length_coxa);
        }
        joint_socket(); // Proximal socket attachment
    }
}

if (part_type == "FEMUR") {
    difference() {
        union() {
            cylinder(h = length_femur, r = radius * 1.1);
            joint_ball(length_femur);
        }
        joint_socket();
    }
}

if (part_type == "TIBIA") {
    difference() {
        union() {
            cylinder(h = length_tibia, r = radius * 0.9);
            joint_ball(length_tibia);
        }
        joint_socket();
    }
}
