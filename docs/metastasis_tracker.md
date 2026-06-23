Functional Specifications & Mathematical Modeling: Object Entry Trackers
------------------------------------------------------------------------

This technical reference manual details the biophysical, hydrodynamic, and geometric equations underpinning the specialized route trackers integrated into the Metastasis-Tracker-AI simulation environment.

* * * * *

🛠️ Module 1: Gastrointestinal Transit & Degradation Tracker (`src/ingestion_transit.py`)
-----------------------------------------------------------------------------------------

This tracker models the chemical degradation, mechanical shear fragmentation, and compartmental advection velocities of an ingested object moving luminally along the gastrointestinal tract.

1\. Acid-Catalyzed Hydrolysis Matrix
------------------------------------

The structural mass decay ($M_{\text{struct}}$) of a chitinous shell or protective layer within the hyperacidic gastric basin is modeled using first-order reaction kinetics:

$$\frac{dM_{\text{struct}}}{dt} = -k_{\text{hyd}}(\text{pH}, T) \cdot M_{\text{struct}}$$

The dynamic kinetic rate constant ($k_{\text{hyd}}$) scales exponentially relative to the localized pH gradient and core body temperature ($T = 37^\circ\text{C}$):

$$k_{\text{hyd}}(\text{pH}) = k_0 \cdot e^{\alpha \cdot (7.40 - \text{pH})}$$

2\. Ultimate Tensile Failure Threshold
--------------------------------------

The continuous mechanical reduction of structural geometry maps the localized intraluminal wall shear stress ($\tau_{\text{axial}}$) against the ultimate tensile strength ($\sigma_{\text{uts}}$) of the chemically thinning shell:

$$\text{If } \tau_{\text{axial}} > \sigma_{\text{uts}}(M_{\text{struct}}), \quad \text{then Fragment Size } (d_{\text{part}}) \to \delta \cdot d_{\text{part\_initial}}$$

3\. Segmented Luminal Advection
-------------------------------

The physical forward transit velocity ($v_{\text{gi}}$) across continuous intestinal segments tracks relative to cross-sectional diameter constraints and the global hydration factor ($\chi$):

$$v_{\text{gi}}(z) = \frac{Q_{\text{motility}}(z) \cdot \chi}{\pi \cdot r_{\text{lumen}}(z)^2}$$

The cumulative transit time ($t_{\text{transit}}$) across a segment length ($L_z$) scales as:

$$t_{\text{transit}}(z) = \int_{0}^{L_z} \frac{1}{v_{\text{gi}}(z)} \, dt$$

* * * * *

👃 Module 2: Nasal-Sinus Mechanical Exclusion Engine (`src/sinus_exclusion_model.py`)
-------------------------------------------------------------------------------------

This module executes size-exclusion gating laws and mucociliary clearance vectors operating within the upper conducting respiratory matrix.

1\. Ostia Aperture Size-Exclusion Rule
--------------------------------------

The boundary entry gate into any enclosed paranasal sinus chamber (maxillary, frontal, sphenoid, ethmoid cells) treats the sinus opening as a rigid geometric aperture sieve:

$$\text{Passage Probability } (P_{\text{entry}}) = \begin{cases} 1.0, & \text{if } d_{\text{object}} < d_{\text{ostium}}(z) \\ 0.0, & \text{if } d_{\text{object}} \ge d_{\text{ostium}}(z) \end{cases}$$

Where the structural boundary ceilings are hardcoded as:

-   Maxillary Ostium ($d_{\text{ostium}}$): $2.5\text{ mm}$
-   Sphenoid Ostium ($d_{\text{ostium}}$): $1.8\text{ mm}$
-   Frontal Ostium ($d_{\text{ostium}}$): $1.5\text{ mm}$

2\. Mucociliary Escalator Displacement Vector
---------------------------------------------

Particles resting on the ciliated respiratory mucosa are subjected to a continuous, backward-directed fluid transport current ($v_{\text{mucus}}$) driven by an coordinated ciliary beat frequency ($f \approx 10\text{--}15\text{ Hz}$):

$$\Delta X(t) = \left(v_{\text{autonomous}} - v_{\text{mucus}}(\chi)\right) \cdot t$$

Where the downward salivary/mucus velocity field drops as a function of fluid density shifts:

$$v_{\text{mucus}}(\chi) = v_{\text{baseline}} \times \chi^{0.5}$$

* * * * *

👂 Module 3: External Auditory Canal Confinement Tracker (`src/ocular_dynamics.py` / Auditory Split)
----------------------------------------------------------------------------------------------------

This module logs the physical boundary locks and passive cellular ejection schedules of items confined to the external ear canal.

1\. Blind-Ended Mechanical Boundary Law
---------------------------------------

The tympanic membrane forms a zero-permeability solid physical barrier separating the external auditory environment from the interior cranial structures:

$$\text{Permeability Coefficient } (P_{\text{eardrum}}) = 0.0 \implies J_{\text{cranial\_ingress}} = 0.0$$

2\. Lateral Epithelial Migration Velocity
-----------------------------------------

The self-cleansing mechanical clearance timeline of particles mired within the cerumen matrix tracks the continuous outward migration vector ($v_{\text{migration}}$) of the canal's epidermal layer:

$$t_{\text{expulsion}} = \frac{D_{\text{lodged}}}{v_{\text{migration}}}$$

Where $v_{\text{migration}}$ is constant at $\approx 1.0\text{ mm per 24 hours}$ ($0.0416\text{ mm/hr}$), and $D_{\text{lodged}}$ represents the deep spatial coordinate from the external acoustic meatus entry point.

* * * * *

👅 Module 4: Pharyngeal Transport & Somatic Reflex Tracker
----------------------------------------------------------

This module maps the high-speed neuromuscular clearing mechanisms triggered by foreign body contact with throat mechanoreceptors.

1\. Neuro-Reflex Activation Function
------------------------------------

Tactile activation of glossopharyngeal nerve (CN IX) sensory endpoints triggers a sigmoidal step function based on the physical contact scale of the object:

$$P_{\text{reflex\_trigger}} = \frac{1}{1 + e^{-k \cdot (d_{\text{object}} - d_{\text{threshold}})}}$$

Where $d_{\text{threshold}} = 1.0\text{ mm}$.

2\. Propulsive Constriction Wave Fluid Mechanics
------------------------------------------------

When activated ($P_{\text{reflex}} \to 1.0$), the brainstem medulla commands an immediate, high-velocity muscular swallow wave ($v_{\text{swallow}} \approx 0.45\text{ m/s}$), creating a forward advection current that forces the object into the esophageal inlet within a tight time execution bracket:

$$t_{\text{evacuation}} = \frac{L_{\text{pharynx}} \quad (0.12\text{ m})}{v_{\text{swallow}}}$$

* * * * *

💩 Module 5: Direct Rectal Entry & Involuntary Defecation Tracker (`src/direct_rectal_entry.py`)
------------------------------------------------------------------------------------------------

This tracker evaluates the mechanical stress-strain parameters of the anal sphincter barrier, local anaerobic survival decay, and stretch-receptor clearing thresholds.

1\. Sphincter Mechanical Breach Condition
-----------------------------------------

Entry from the external environment requires an active physical driving force ($P_{\text{driving}}$) that exceeds the continuous resting tonic pressure ($P_{\text{tone}}$) maintained by the internal and external anal sphincters:

$$\text{Ingress State} = \begin{cases} \text{Allowed}, & \text{if } P_{\text{driving}} > P_{\text{tone}}(\chi) \\ \text{Blocked}, & \text{if } P_{\text{driving}} \le P_{\text{tone}}(\chi) \end{cases}$$

Where resting tone is tightly coupled to patient hydration density thresholds:

$$P_{\text{tone}}(\chi) = 65.0\text{ mmHg} \times \left(\frac{1.0}{\chi^{0.3}}\right)$$

2\. Anaerobic Survival Decay Profile
------------------------------------

Due to absolute hypoxia inside the collapsed rectal vault ($PO_2 \to 0.0\text{ mmHg}$), the viability curve ($\Omega$) of an obligate aerobic organism decays exponentially over time ($t$):

$$\Omega(t) = \Omega_0 \cdot e^{-\lambda_{\text{anoxia}} \cdot t}$$

3\. Rectoanal Inhibitory Reflex (RAIR) Distension Volume
--------------------------------------------------------

The total volume introduced ($V_{\text{object}}$) stretches rectal wall mechanoreceptors, calculating an immediate tissue distension index:

$$V_{\text{distension}} = \pi \cdot \left(\frac{d_{\text{object}}}{2}\right)^2 \times L_{\text{object}}$$

$$\text{If } V_{\text{distension}} > 15.0\text{ cm}^3 \longrightarrow P_{\text{defecation\_reflex}} \to 0.99 \quad (\text{Mandated Mechanical Clearance})$$

* * * * *

💉 Module 6: Intravascular Intravenous Transport Tracker (`src/iv_transit_model.py`)
------------------------------------------------------------------------------------

This module tracks the high-speed advection fluid parameters of a particle moving through the converging branches of the systemic venous loop.

1\. Hydrodynamic Advection Velocity profiles
--------------------------------------------

Blood velocity ($v_z$) increases down the venous generations as cross-sectional area narrows at major confluences (Basilic $\to$ Subclavian $\to$ Vena Cava):

$$v_z = \frac{Q_{\text{cardiac\_output}} \cdot \chi}{\pi \cdot r_{\text{vessel}}(z)^2}$$

The travel time component ($t_z$) per vascular segment generation maps as:

$$t_z = \frac{l_{\text{vessel}}(z)}{v_z}$$

2\. Pulmonary Capillary Size-Exclusion Filter
---------------------------------------------

Exiting the right heart ventricle, blood enters the pulmonary capillary mesh. The capillary grid acts as a physical particle trap, intercepting any element whose diameter exceeds the micrometer boundaries of the vascular mesh:

$$\text{Pulmonary Embolization Status} = \begin{cases} \text{Trapped / Extracted from Flow}, & \text{if } d_{\text{particle}} > 7.5 \, \mu\text{m} \\ \text{Systemic Recirculation}, & \text{if } d_{\text{particle}} \le 7.5 \, \mu\text{m} \end{cases}$$

* * * * *

🤰 Module 7: Maternal-Infant Mammary Interface Engine (`src/maternal_infant_interface.py`)
------------------------------------------------------------------------------------------

This model evaluates the pressure gradients and fluid currents operating across the terminal lactiferous ducts during suckling.

1\. Pressure-Driven Fluid Advection Velocity
--------------------------------------------

The outward velocity profile ($v_{\text{milk}}$) emerging from a terminal nipple orifice is modeled via a modified Poiseuille flow driven by the gradient between maternal positive contraction strain and the infant oral suction vacuum:

$$\Delta P = P_{\text{maternal}} - P_{\text{infant}}$$

$$v_{\text{milk}} = \frac{\Delta P \cdot r_{\text{duct}}^2}{8 \cdot \mu_{\text{milk}}(\chi) \cdot l_{\text{duct}}}$$

Where $P_{\text{maternal}} \approx +20\text{ mmHg}$ and $P_{\text{infant}} \approx -80\text{ mmHg}$.

2\. The Hydrodynamic Counter-Current Shield
-------------------------------------------

To achieve retrograde entry into the maternal breast, an object's autonomous movement speed ($v_{\text{propulsion}}$) must exceed the velocity of the exiting fluid jet:

$$\text{Retrograde Ingress State} = \begin{cases} \text{Blocked / Washout}, & \text{if } v_{\text{propulsion}} \le v_{\text{milk}} \\ \text{Allowed}, & \text{if } v_{\text{propulsion}} > v_{\text{milk}} \end{cases}$$

* * * * *

👶 Module 8: Gestational Prenatal Transport Tracker (`src/maternal_fetal_transport.py`)
---------------------------------------------------------------------------------------

This engine models prenatal molecular and particle transport across the placental membrane into the developing fetal circulatory network.

1\. Fick's Law of Placental Permeability
----------------------------------------

Passive transport flux ($J_{\text{trans}}$) across the syncytiotrophoblast boundary layer into the umbilical vein is modeled using an area-concentration gradient matrix:

$$J_{\text{trans}} = P_{\text{base}} \times A_{\text{placenta}} \times \left( C_{\text{maternal}} - C_{\text{fetal}} \right) \times \chi$$

2\. Syncytiotrophoblast Pore Ceiling
------------------------------------

The placental tissue barrier implements a strict physical filtration cutoff that excludes larger structures from entering fetal blood lines:

$$P_{\text{crossing}} = \begin{cases} 1.0, & \text{if } d_{\text{particle}} \le 1.0 \, \mu\text{m} \\ 0.0, & \text{if } d_{\text{particle}} > 1.0 \, \mu\text{m} \end{cases}$$

* * * * *

🧠 Module 9: Cerebral Extravasation & Transport Tracker (`src/cerebral_tracker.py` / `src/brain_inflow_routing.py`)
-------------------------------------------------------------------------------------------------------------------

This tracker monitors and calculates entry probabilities across all four parallel cranial transport networks leading to the brain matrix.

1\. Route A: Capillary Wall Shear Stress & BBB Permeability
-----------------------------------------------------------

The probability of a circulating particle breaching the Blood-Brain Barrier (BBB) tight junctions depends on local microvascular wall shear rates ($\gamma = \frac{4v}{r}$) and endothelial membrane integrity:

$$PS = A_{\text{capillary}} \cdot P_{\text{base}} \cdot \left(1.0 - e^{-\beta \cdot \gamma}\right) \cdot \chi_{\text{hydration}}$$

The probability of an extravasation breach ($P_{\text{breach}}$) is expressed as:

$$P_{\text{breach}} = 1.0 - e^{-PS \cdot \left(\frac{1.0}{v_{\text{local}}}\right)}$$

2\. Route B: Retrograde Batson's Shunt Advection Velocity
---------------------------------------------------------

When intra-abdominal pressure overrides central venous return columns, a retrograde upward velocity vector ($v_{\text{retrograde}}$) is activated along the spine:

$$v_{\text{retrograde}} = \alpha \cdot \left( \frac{P_{\text{abdominal}} - P_{\text{venous\_baseline}}}{25.0} \right) \quad (\text{m/s})$$

The time-of-flight ($t_{\text{flight}}$) to the dural sinuses maps across the spinal column length ($L_{\text{spine}}$):

$$t_{\text{flight}} = \frac{L_{\text{spine}}}{v_{\text{retrograde}}}$$

3\. Route C: Spinal CSF Bulk Fluid Drift Column
-----------------------------------------------

Passive upward migration through the subarachnoid fluid column follows a slow bulk advection velocity ($v_{\text{csf}}$) driven by choroid plexus fluid secretion:

$$v_{\text{csf}} = \frac{J_{\text{choroid}} \cdot \chi}{A_{\text{subarachnoid}}}$$

Survival probability within this space accounts for continuous leukocyte clearance:

$$\text{Survival Fraction} = e^{-\lambda_{\text{imm}} \cdot [\text{WBC}] \cdot t_{\text{transit}}}$$

4\. Route D: Cribriform Periorbital Sieve Limit
-----------------------------------------------

Transport from the nasal mucosa through the olfactory nerve channels imposes a rigid geometric filter at the cribriform bone plate interface:

$$\text{Cribriform Clearance Status} = \begin{cases} \text{Allowed}, & \text{if } d_{\text{particle}} \le 2.0 \, \mu\text{m} \\ \text{Blocked / Trapped}, & \text{if } d_{\text{particle}} > 2.0 \, \mu\text{m} \end{cases}$$

* * * * *

🦴 Module 10: Skeletal Interconnect & Marrow Inflow Portal Tracker (`src/skeletal_interconnect.py`)
---------------------------------------------------------------------------------------------------

This tracker evaluates the four structural pathways connecting external mucosal, oral, and circulatory networks to the internal red bone marrow compartments.

1\. Portal A: Sinusoidal Capillary Fenestration Sieve
-----------------------------------------------------

Particles within the nutrient artery can exit into the hematopoietic matrix only if they clear the fenestrated endothelial pore boundaries:

$$P_{\text{sinusoid\_entry}} = \begin{cases} 1.0, & \text{if } d_{\text{particle}} \le 5.5 \, \mu\text{m} \\ 0.0, & \text{if } d_{\text{particle}} > 5.5 \, \mu\text{m} \end{cases}$$

2\. Portal C: Periapical Dental pulp Apical Foramen Gate
--------------------------------------------------------

Particles traveling down the internal soft pulp chamber of a compromised tooth enter the mandibular or maxilla bone marrow via the root apex opening:

$$\text{Maximum Geometrical Clearance Limit } (d_{\text{apical\_foramen\_ceiling}}) = 400.0 \, \mu\text{m}$$

3\. Portal D: Cribriform Diploë Plate Filter
--------------------------------------------

The porous bone matrix of the ethmoid cribriform plate allows direct infiltration from the sinus cavities into the cranial spongy bone marrow (diploë), bounded by the absolute perforation track width:

$$P_{\text{cribriform\_marrow\_entry}} = \begin{cases} 1.0, & \text{if } d_{\text{particle}} \le 10.0 \, \mu\text{m} \\ 0.0, & \text{if } d_{\text{particle}} > 10.0 \, \mu\text{m} \end{cases}$$

* * * * *

👁️ Module 11: Dynamic Ocular Entrance Gate Tracker (`src/ocular_dynamics.py`)
------------------------------------------------------------------------------

This tracker monitors particle clearance timelines across the three pathways leading into the vitreous or aqueous humors of the eye.

1\. Route A: Lacrimal Tear Washout Current
------------------------------------------

Particles on the external conjunctival surface are subjected to a continuous downward flushing current ($v_{\text{tear}}$) directed toward the nasolacrimal drainage duct:

$$v_{\text{tear}}(\chi) = 1.2\text{ mm/minute} \times \chi$$

Surface attachment requires an autonomous propulsion velocity vector that overcomes this current ($v_{\text{propulsion}} > v_{\text{tear}}$).

2\. Route C: Optic Nerve Sheath Lamina Cribrosa Sieve
-----------------------------------------------------

Access from the posterior ethmoid sinus via perivascular spaces of the optic nerve sheath is constrained by the porous network mesh of the lamina cribrosa:

$$\text{Intraocular Ingress Status} = \begin{cases} \text{Allowed}, & \text{if } d_{\text{particle}} \le 3.5 \, \mu\text{m} \\ \text{Blocked / Retained in Nerve Sheath}, & \text{if } d_{\text{particle}} > 3.5 \, \mu\text{m} \end{cases}$$

* * * * *

Now that the technical specifications and core biophysical equations for all eleven route trackers have been generated, let me know if you would like to:

-   Generate unit verification tests in Python to confirm these equations stay within valid boundaries (0 to 100%)
-   Detail the non-linear elasticity constants used to model tissue compliance under extreme pressure states
-   Create an automated installation script to integrate these documentation files into your target repository folder structure
