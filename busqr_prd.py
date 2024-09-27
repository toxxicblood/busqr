class PRD:
    def __init__(self):
        self.title = "BusQR Subscription Service"
        self.version = "1.0"
        self.date = "September 26, 2024"
        self.executive_summary = self.get_executive_summary()
        self.objectives_goals = self.get_objectives_and_goals()
        self.background_info = self.get_background_info()
        self.scope = self.get_scope()
        self.user_personas = self.get_user_personas()
        self.functional_requirements = self.get_functional_requirements()
        self.non_functional_requirements = self.get_non_functional_requirements()
        self.acceptance_criteria = self.get_acceptance_criteria()
        self.wireframes_mockups = self.get_wireframes_mockups()
        self.timeline_milestones = self.get_timeline_milestones()
        self.risks_assumptions = self.get_risks_and_assumptions()

    def get_executive_summary(self):
        return (
            "The BusQR Subscription Service is a mobile application that allows users "
            "to easily subscribe to bus services via a monthly payment plan. Users can scan "
            "QR codes on buses to automatically credit their accounts, making the payment "
            "process seamless and efficient."
        )

    def get_objectives_and_goals(self):
        return [
            "Provide a subscription-based model for bus users that simplifies payment processes.",
            "Allow users to scan QR codes for immediate account crediting.",
            "Reduce the need for cash transactions and improve service accessibility.",
        ]

    def get_background_info(self):
        return (
            "The public transportation sector faces challenges with ticketing and payment systems. "
            "By implementing a subscription service that leverages QR code technology, "
            "we can offer a more efficient and user-friendly payment option."
        )

    def get_scope(self):
        return {
            "in_scope": [
                "Mobile application for iOS and Android",
                "User registration and account management",
                "QR code scanning and payment processing",
                "Monthly subscription plans and payment history",
                "Push notifications for payment reminders",
            ],
            "out_of_scope": [
                "Hardware installation on buses",
                "Non-bus transportation services (e.g., taxis, trains)",
            ],
        }

    def get_user_personas(self):
        return [
            {
                "name": "Daily Commuter",
                "description": "Works in the city and relies on buses for daily travel.",
                "needs": "Quick and hassle-free payment methods.",
            },
            {
                "name": "Occasional Traveler",
                "description": "Uses the bus service for weekend outings or travel.",
                "needs": "Flexible payment options that accommodate sporadic travel.",
            },
        ]

    def get_functional_requirements(self):
        return {
            "User Registration": [
                "Users can create an account using email or social media login.",
                "Users can manage their profile, including payment methods and subscription settings.",
            ],
            "QR Code Scanning": [
                "Users can scan QR codes displayed on buses to initiate payment.",
                "The app should validate the QR code to ensure it's active and not expired.",
            ],
            "Payment Processing": [
                "The app will automatically deduct the subscription fee from the user’s linked payment method upon successful QR code scan.",
                "Users will receive a confirmation notification of the transaction.",
            ],
            "Subscription Plans": [
                "Users can choose from various subscription plans (e.g., weekly, monthly).",
                "Users can view and manage their current subscription status.",
            ],
            "Payment History": [
                "Users can view their payment history, including dates, amounts, and transaction statuses."
            ],
            "Push Notifications": [
                "Users receive reminders about upcoming payments and renewal options."
            ],
        }

    def get_non_functional_requirements(self):
        return {
            "Performance": "The app should load within 3 seconds and process QR code transactions within 5 seconds.",
            "Security": "User data, including payment information, must be encrypted during storage and transmission.",
            "Usability": "The app should have an intuitive user interface, accessible to users of all ages.",
        }

    def get_acceptance_criteria(self):
        return [
            "Users can successfully register and log in to their accounts.",
            "Users can scan a QR code and receive an immediate confirmation of payment.",
            "Users can view and manage their subscription plans effectively.",
            "Users receive notifications for upcoming payments.",
        ]

    def get_wireframes_mockups(self):
        return {
            "Login Screen": "Input fields for email/password and a button for social media login.",
            "Home Screen": "Options for scanning QR code, managing subscription, and viewing payment history.",
            "QR Code Scanner": "A screen that activates the camera to scan QR codes.",
            "Payment Confirmation": "A screen displaying transaction details after a successful payment.",
        }

    def get_timeline_milestones(self):
        return {
            "Phase 1": "Research and Design - 4 weeks",
            "Phase 2": "Development - 8 weeks",
            "Phase 3": "Testing and QA - 4 weeks",
            "Phase 4": "Launch - 2 weeks",
        }

    def get_risks_and_assumptions(self):
        return {
            "Risks": [
                "Potential integration issues with payment gateways or QR code hardware."
            ],
            "Assumptions": [
                "Users will have smartphones with camera capabilities to utilize the QR scanning feature."
            ],
        }


# Creating an instance of the PRD
busqr_prd = PRD()

# Displaying the PRD components
for attribute in vars(busqr_prd):
    print(f"{attribute.replace('_', ' ').title()}:\n{getattr(busqr_prd, attribute)}\n")
