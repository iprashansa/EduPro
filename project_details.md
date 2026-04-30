Instructor Performance and Course Quality Evaluation on EduPro
Detailed guide and project requirements for the Instructor Performance and Course Quality Evaluation on EduPro analysis.
Background and Context:
In online education, instructor quality and course design are the strongest drivers of:
• Learner satisfaction
• Course ratings
• Repeat enrollments
• Platform credibility
Even with strong learner demand, poor instructional quality can lead to:
• Low course ratings
• Negative reviews
• Reduced trust in the platform
EduPro needs a data-driven framework to evaluate:
• Instructor effectiveness
• Course quality consistency
• Relationship between teaching expertise and learner satisfaction

Unified Mentor
Toronto Government Parks, Forestry & Recreation
Problem Statement
Currently, EduPro lacks clarity on:

• Which instructors consistently deliver high-quality courses?

• Does teaching experience translate into better-rated courses?

• Are some course categories more dependent on instructor quality?

• How evenly is teaching performance distributed across the platform?
Without structured analysis, instructor evaluation remains subjective and fragmented.
Dataset Fields Utilized (High-Dimensional)
Teachers Sheet
• TeacherID
• TeacherName
• Age
• Gender
• Expertise
• YearsOfExperience
• TeacherRating
Courses Sheet
• CourseID
• CourseName
• CourseCategory
• CourseLevel
• CourseRating
Transactions Sheet
• TransactionID
• CourseID
• TeacherID
Key Analytical Questions
This project aims to answer:

• What is the overall distribution of instructor ratings?

• Do instructors with more experience receive higher ratings?

• Is there a relationship between TeacherRating and CourseRating?

• Which expertise areas consistently deliver high-quality courses?

• Are highly rated instructors associated with higher enrollments?
Analytical Methodology (Step-by-Step)
Data Integration
• Join Teachers ↔ Courses ↔ Transactions using TeacherID and CourseID
• Validate mapping between instructors and their courses
Instructor Profile Analysis
• Distribution of instructor age, experience, and expertise
• Rating spread across instructors
• Identification of top-performing and low-performing instructors
Experience vs Performance Analysis
• Correlation between:
○ YearsOfExperience and TeacherRating
○ YearsOfExperience and CourseRating
• Identify diminishing returns or experience thresholds
Course Quality Evaluation
• CourseRating analysis by:
○ CourseCategory
○ CourseLevel
• Gender vs course level comparisons
• Identify categories with consistently high or low ratings
Instructor Impact on Course Success
• Compare course ratings for:
○ High-rated instructors
○ Mid-rated instructors
○ Low-rated instructors
• Enrollment volume comparison by instructor rating tier
Expertise-Based Performance Insights
• Instructor expertise vs course quality
• Identify domains where teaching quality is most critical
• Highlight expertise gaps or training needs
Key Performance Indicators (KPIs)
KPI NameDescriptionAverage Teacher RatingTeaching quality benchmarkAverage Course RatingContent effectivenessRating Consistency IndexInstructor reliabilityExperience Impact ScoreValue of teaching tenureEnrollment Influence RatioInstructor-driven demand
Streamlit Web Application Requirements
Core Modules
• Instructor performance leaderboard
• Experience vs rating scatter plots
• Course quality heatmaps
• Expertise-wise performance comparisons
User Capabilities
• Instructor expertise filters
• Course category & level selectors
• Rating range sliders
Deliverables and Submission
• Research paper (EDA, insights, recommendations)

• Streamlit dashboard (live analytics)

• Executive summary for government stakeholders
Conclusion
This project establishes a data-driven instructor and course quality evaluation framework for EduPro. By shifting focus away from learners and toward teaching effectiveness, it enables the platform to identify excellence, address gaps, and continuously improve educational outcomes—making it fundamentally different in purpose.


For the tech stack i'm open for anything in python but for the web MERN is what i have worked on before but i'm open for next.js 