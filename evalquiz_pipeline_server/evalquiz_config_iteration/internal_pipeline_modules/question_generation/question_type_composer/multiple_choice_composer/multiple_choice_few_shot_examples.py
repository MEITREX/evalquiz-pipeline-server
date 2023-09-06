from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.few_shot_example import (
    FewShotExample,
)
from evalquiz_proto.shared.generated import (
    Capability,
    EducationalObjective,
    MultipleChoice,
    Question,
    QuestionType,
    Relationship,
    Result,
)

few_shot_example_filtered_text_1 = """2Scrum Definition
Scrum is a lightweight framework that helps people, teams and organizations generate value through
adaptive solutions for complex problems.
In a nutshell, Scrum requires a Scrum Master to foster an environment where:
1.
The Scrum Team turns a selection of the work into an Increment of value during a Sprint.
The Scrum Team and its stakeholders inspect the results and adjust for the next Sprint.
A
Scrum Team is expected to adapt the moment it learns anything new through inspection.
Scrum Values
Successful use of Scrum depends on people becoming more proficient in living five values:
Commitment, Focus, Openness, Respect, and Courage
The Scrum Team commits to achieving its goals and to supporting each other.
The Scrum Team and its
stakeholders are open about the work and the challenges.
Scrum Team members respect each other to
be capable, independent people, and are respected as such by the people with whom they work.
The
Scrum Team members have the courage to do the right thing, to work on tough problems.
These values give direction to the Scrum Team with regard to their work, actions, and behavior.
The Scrum Team members learn and explore the values as they work with
the Scrum events and artifacts.
When these values are embodied by the Scrum Team and the people
they work with, the empirical Scrum pillars of transparency, inspection, and adaptation come to life
building trust.
4Scrum Team
The fundamental unit of Scrum is a small team of people, a Scrum Team.
The Scrum Team consists of
one Scrum Master, one Product Owner, and Developers.
Within a Scrum Team, there are no sub-teams
or hierarchies.
Scrum Teams are cross-functional, meaning the members have all the skills necessary to create value
each Sprint.
The Scrum Team is small enough to remain nimble and large enough to complete significant work within
a Sprint, typically 10 or fewer people.
In general, we have found that smaller teams communicate better
and are more productive.
If Scrum Teams become too large, they should consider reorganizing into
multiple cohesive Scrum Teams, each focused on the same product.
The Scrum Team is responsible for all product-related activities from stakeholder collaboration,
verification, maintenance, operation, experimentation, research and development, and anything else
that might be required.
Working in Sprints at a sustainable pace improves the Scrum Team’s focus and consistency.
The entire Scrum Team is accountable for creating a valuable, useful Increment every Sprint.
Scrum
defines three specific accountabilities within the Scrum Team: the Developers, the Product Owner, and
the Scrum Master.
Developers
Developers are the people in the Scrum Team that are committed to creating any aspect of a usable
Increment each Sprint.
Scrum Master
The Scrum Master is accountable for establishing Scrum as defined in the Scrum Guide.
The Scrum Master is accountable for the Scrum Team’s effectiveness.
Scrum Masters are true leaders who serve the Scrum Team and the larger organization.
The Scrum Master serves the Scrum Team in several ways, including:
●
●
●
●
Coaching the team members in self-management and cross-functionality;
Helping the Scrum Team focus on creating high-value Increments that meet the Definition of
Done;
Causing the removal of impediments to the Scrum Team’s progress; and,
Ensuring that all Scrum events take place and are positive, productive, and kept within the
timebox.
The Scrum Master serves the Product Owner in several ways, including:
6●
●
●
●
Helping find techniques for effective Product Goal definition and Product Backlog management;
Helping the Scrum Team understand the need for clear and concise Product Backlog items;
Helping establish empirical product planning for a complex environment; and,
Facilitating stakeholder collaboration as requested or needed.
The Scrum Master serves the organization in several ways, including:
●
●
●
●
Leading, training, and coaching the organization in its Scrum adoption;
Planning and advising Scrum implementations within the organization;
Helping employees and stakeholders understand and enact an empirical approach for complex
work; and,
Removing barriers between stakeholders and Scrum Teams.
The whole Scrum Team then collaborates to define a Sprint Goal that communicates why the Sprint is
valuable to stakeholders.
If the Product Owner or Scrum Master
are actively working on items in the Sprint Backlog, they participate as Developers.
Based on this information, attendees collaborate on what to do
next.
If the work turns out to be
different than they expected, they collaborate with the Product Owner to negotiate the scope of the
Sprint Backlog within the Sprint without affecting the Sprint Goal.
"""

few_shot_example_filtered_text_2 = """We are humbled to see
Scrum being adopted in many domains holding essentially complex work, beyond software product
development where Scrum has its roots.
A Product Owner orders the work for a complex problem into a Product Backlog.
Adaptation
If any aspects of a process deviate outside acceptable limits or if the resulting product is unacceptable,
the process being applied or the materials being produced must be adjusted.
The Scrum Team consists of
one Scrum Master, one Product Owner, and Developers.
It is a cohesive unit of professionals focused on one objective at a time, the Product Goal.
In general, we have found that smaller teams communicate better
and are more productive.
If Scrum Teams become too large, they should consider reorganizing into
multiple cohesive Scrum Teams, each focused on the same product.
Therefore, they should share the
same Product Goal, Product Backlog, and Product Owner.
The Scrum Team is responsible for all product-related activities from stakeholder collaboration,
verification, maintenance, operation, experimentation, research and development, and anything else
that might be required.
Scrum
defines three specific accountabilities within the Scrum Team: the Developers, the Product Owner, and
the Scrum Master.
Product Owner
The Product Owner is accountable for maximizing the value of the product resulting from the work of
the Scrum Team.
5The Product Owner is also accountable for effective Product Backlog management, which includes:
●
●
●
●
Developing and explicitly communicating the Product Goal;
Creating and clearly communicating Product Backlog items;
Ordering Product Backlog items; and,
Ensuring that the Product Backlog is transparent, visible and understood.
The Product Owner may do the above work or may delegate the responsibility to others.
Regardless, the
Product Owner remains accountable.
For Product Owners to succeed, the entire organization must respect their decisions.
These decisions
are visible in the content and ordering of the Product Backlog, and through the inspectable Increment at
the Sprint Review.
The Product Owner is one person, not a committee.
The Product Owner may represent the needs of
many stakeholders in the Product Backlog.
Those wanting to change the Product Backlog can do so by
trying to convince the Product Owner.
The Scrum Master serves the Scrum Team in several ways, including:
●
●
●
●
Coaching the team members in self-management and cross-functionality;
Helping the Scrum Team focus on creating high-value Increments that meet the Definition of
Done;
Causing the removal of impediments to the Scrum Team’s progress; and,
Ensuring that all Scrum events take place and are positive, productive, and kept within the
timebox.
The Scrum Master serves the Product Owner in several ways, including:
6●
●
●
●
Helping find techniques for effective Product Goal definition and Product Backlog management;
Helping the Scrum Team understand the need for clear and concise Product Backlog items;
Helping establish empirical product planning for a complex environment; and,
Facilitating stakeholder collaboration as requested or needed.
All the work necessary to achieve the Product Goal, including Sprint Planning, Daily Scrums, Sprint
Review, and Sprint Retrospective, happen within Sprints.
During the Sprint:
●
●
●
●
No changes are made that would endanger the Sprint Goal;
Quality does not decrease;
The Product Backlog is refined as needed; and,
Scope may be clarified and renegotiated with the Product Owner as more is learned.
Sprints enable predictability by ensuring inspection and adaptation of progress toward a Product Goal at
least every calendar month.
Only the Product Owner has the
authority to cancel the Sprint.
The Product Owner ensures that attendees are prepared to discuss the most important Product Backlog
items and how they map to the Product Goal.
The Product Owner proposes how the product could increase its value and utility in the current Sprint.
Through discussion with the Product Owner, the Developers select items from the Product Backlog to
include in the current Sprint.
For each selected Product Backlog item, the Developers plan the work necessary to create an Increment
that meets the Definition of Done.
This is often done by decomposing Product Backlog items into
smaller work items of one day or less.
No
one else tells them how to turn Product Backlog items into Increments of value.
8The Sprint Goal, the Product Backlog items selected for the Sprint, plus the plan for delivering them are
together referred to as the Sprint Backlog.
If the Product Owner or Scrum Master
are actively working on items in the Sprint Backlog, they participate as Developers.
The Scrum Team presents the results of their work to key stakeholders and progress
toward the Product Goal is discussed.
The Product Backlog may also be adjusted to meet new opportunities.
"""

few_shot_example_1 = FewShotExample(
    Question(
        QuestionType.MULTIPLE_CHOICE,
    ),
    [
        Capability(
            ["scrum", "master"],
            EducationalObjective.KNOW_AND_UNDERSTAND,
            Relationship.COMPLEX,
        )
    ],
    few_shot_example_filtered_text_1,
    Result(
        multiple_choice=MultipleChoice(
            "Which of the following is true about the Scrum Master?",
            "The Scrum Master is part of the Scrum Team.",
            [
                "The Scrum Master is not accountable for the Scrum Team’s effectiveness.",
                "The Scrum Master develops how the product should look like.",
            ],
        )
    ),
)

few_shot_example_2 = FewShotExample(
    Question(
        QuestionType.MULTIPLE_CHOICE,
    ),
    [
        Capability(
            ["product", "owner"],
            EducationalObjective.KNOW_AND_UNDERSTAND,
            Relationship.COMPLEX,
        )
    ],
    few_shot_example_filtered_text_2,
    Result(
        multiple_choice=MultipleChoice(
            "What is a responsibility of the Product Owner?",
            "Maximizing the value of the product.",
            [
                "Writing most of the implementation code.",
                "Ensure that all Scrum events take place, and are held in a positive manner.",
            ],
        )
    ),
)

multiple_choice_few_shot_examples = [few_shot_example_1, few_shot_example_2]
