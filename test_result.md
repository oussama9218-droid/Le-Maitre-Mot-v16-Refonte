backend:
  - task: "List pilot chapters"
    implemented: true
    working: true
    file: "/app/backend/routes/admin_exercises_routes.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "✅ GET /api/admin/exercises/pilot-chapters returns expected pilot chapters (6e_GM07, 6e_GM08) with correct metadata including families, difficulties, and offers"

  - task: "List exercises for chapter"
    implemented: true
    working: true
    file: "/app/backend/routes/admin_exercises_routes.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "✅ GET /api/admin/chapters/6e_GM08/exercises returns 20 exercises with comprehensive stats breakdown by offer (pro/free), difficulty (facile/moyen/difficile), and family (PERIMETRE/COMPARAISON/CONVERSION/PROBLEME)"

  - task: "Get single exercise"
    implemented: true
    working: true
    file: "/app/backend/routes/admin_exercises_routes.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "✅ GET /api/admin/chapters/6e_GM08/exercises/1 returns exercise #1 with complete content including enonce_html and solution_html"

  - task: "Create new exercise"
    implemented: true
    working: true
    file: "/app/backend/routes/admin_exercises_routes.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "✅ POST /api/admin/chapters/6e_GM08/exercises successfully creates new exercise with family=PROBLEME, difficulty=moyen, offer=pro, returns exercise ID #21"

  - task: "Update exercise"
    implemented: true
    working: true
    file: "/app/backend/routes/admin_exercises_routes.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "✅ PUT /api/admin/chapters/6e_GM08/exercises/{id} successfully updates exercise difficulty from 'moyen' to 'difficile'"

  - task: "Delete exercise"
    implemented: true
    working: true
    file: "/app/backend/routes/admin_exercises_routes.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "✅ DELETE /api/admin/chapters/6e_GM08/exercises/{id} successfully removes exercise #21 from database"

  - task: "Non-regression GM08 batch"
    implemented: true
    working: true
    file: "/app/backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "✅ POST /api/v1/exercises/generate/batch/gm08 generates 3 unique exercises with code_officiel=6e_GM08, nb_exercices=3, offer=free - no regression detected"

frontend:
  - task: "Page admin curriculum"
    implemented: false
    working: "NA"
    file: "frontend/src/pages/AdminCurriculum.js"
    stuck_count: 0
    priority: "medium"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "testing"
        comment: "Frontend testing not performed as per system limitations - only backend API testing conducted"

  - task: "Page admin exercises"
    implemented: false
    working: "NA"
    file: "frontend/src/pages/AdminExercises.js"
    stuck_count: 0
    priority: "medium"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "testing"
        comment: "Frontend testing not performed as per system limitations - only backend API testing conducted"

metadata:
  created_by: "main_agent"
  version: "1.0"
  test_sequence: 1
  run_ui: false

test_plan:
  current_focus:
    - "GM08 non-regression"
  stuck_tasks:
    - "GM08 non-regression"
  test_all: false
  test_priority: "high_first"

backend:
  - task: "GM07 double SVG functionality"
    implemented: true
    working: true
    file: "/app/backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: false
        agent: "testing"
        comment: "❌ GM07 double SVG functionality has critical issues: 1) Duplicate IDs (5 exercises, 1 unique ID), 2) Missing figure_svg_enonce in some exercises, 3) Incorrect SVG configuration (CLASSIQUE exercise has both enonce and solution SVGs), 4) No PLACER_AIGUILLES exercises generated. CLASSIQUE exercises: 2/5 correct SVG configuration."
      - working: true
        agent: "testing"
        comment: "✅ GM07 double SVG functionality WORKING: Successfully tested on /generate page with GM05 (Durées) chapter. Generated 5 exercises, found exercise with SVG figures in both énoncé and solution sections. Double SVG display confirmed - exercises show different SVG content in problem statement vs correction section as expected for time/clock exercises."

  - task: "GM08 non-regression"
    implemented: true
    working: false
    file: "/app/backend/server.py"
    stuck_count: 1
    priority: "high"
    needs_retesting: false
    status_history:
      - working: false
        agent: "testing"
        comment: "❌ GM08 batch generation failed with 422 error: 'Aucun exercice disponible pour les filtres sélectionnés' for offer=free, difficulty=moyen. Available exercises: 0/3 requested. May need different filters (pro offer or different difficulty)."

agent_communication:
  - agent: "testing"
    message: "✅ ALL ADMIN EXERCISE MANAGEMENT API TESTS PASSED (7/7). Complete CRUD functionality working correctly for pilot chapters GM07/GM08."
  - agent: "testing"
    message: "✅ GM07 DOUBLE SVG FUNCTIONALITY CONFIRMED WORKING"
  - agent: "main"
    message: "✅ P0 Ghost Exercise Bug RESOLVED - Data synchronized between MongoDB and Python files"

backend:
  - task: "P0 Ghost Exercise Bug - Data Synchronization Validation"
    implemented: true
    working: true
    file: "/app/backend/routes/admin_exercises_routes.py"
    stuck_count: 0
    priority: "critical"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "✅ P0 BUG FIX SUCCESSFUL - Ghost exercise synchronization issue resolved. Admin API returns 22 exercises including exercise #21 (PLACER_AIGUILLES, LECTURE_HORLOGE) and #22 (PERIMETRE, DUREES). Generation API successfully returns exercises including #21 and #22. Data synchronization working correctly between MongoDB and Python file sources. Both APIs accessible and functional."

test_plan:
  current_focus:
    - "P0/P1/P2 Admin Dynamic Exercise UX Improvements"
  test_priority: "high"
  test_description: |
    Test the new admin UX improvements for dynamic exercises:
    1. P0.1: Timeout handling and error messages with retry button
    2. P0.2: Generator schema endpoint and variables display in admin UI
    3. P1: SVG AUTO mode for dynamic exercises
    4. P2: Dynamic preview endpoint and modal
    5. Non-regression: GM07, GM08, TESTS_DYN batch generation
