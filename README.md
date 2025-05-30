# 🏨 Hotel Staff Management System

A comprehensive staff management system designed for hotel operations with a luxurious, professional interface.

## ✨ Features

### Core Functionality
- **Staff Authentication**: Secure login system with role-based access control
- **Check-in/Check-out**: Staff attendance tracking with timestamp logging
- **Leave Management**: Request and approve leave applications
- **Report System**: Submit work reports with manager approval workflow
- **Staff Management**: Add, edit, and manage hotel staff (Manager/HR only)
- **Salary Management**: View and update staff compensation
- **Attendance Reports**: Generate comprehensive attendance summaries

### User Roles & Permissions

#### 🎩 Manager (Full Access)
- All system features
- Staff management and hiring
- Report approval and review
- Attendance oversight
- Salary adjustments
- Analytics dashboard

#### 👔 Human Resource (Management Access)
- Staff management (except report approval)
- Attendance tracking and reports
- Leave request management
- Salary administration
- Staff hiring and status updates

#### 📋 Admin (Limited Access)
- Basic attendance operations
- View personal salary information
- Submit leave requests
- Check-in/check-out functionality

#### 🧹 Other Staff (Cleaning, Marketing, Internship)
- Personal attendance tracking
- Leave request submission
- Salary information viewing
- Report submission

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)

### Installation
1. Clone or download all files to a folder
2. Ensure all `.txt` files are in the same directory as the main script
3. Run the application:
```bash
python SistemManajemenKaryawan.py
```

### Login Credentials
Default user accounts are automatically created:

| Role | Username | ID | Password | Access Level |
|------|----------|----|---------| -------------|
| Manager | manager | 1001 | manager123 | Full Access |
| Admin | admin | 1002 | admin123 | Limited Access |
| Human Resource | hr | 1003 | hr123 | Management Access |
| Cleaning Service | cleaning | 1004 | clean123 | Basic Access |
| Marketing | marketing | 1005 | market123 | Basic Access |
| Internship | intern | 1006 | intern123 | Basic Access |

## 📁 File Structure

```
├── SistemManajemenKaryawan.py  # Main application file
├── Staff.txt                  # Staff login credentials
├── Attendance.txt             # Attendance records
├── Leaves.txt                 # Leave requests
├── Reports.txt                # Work reports
├── CheckIn.txt                # Check-in logs
├── final_validation.py        # System validation script
├── launch_app.py             # Application launcher
└── README.md                 # This file
```

## 🎨 Interface Features

- **Luxury Hotel Theme**: Professional gold and dark color scheme
- **Tabbed Interface**: Organized by access level (Essential, Management, Executive)
- **Role-based UI**: Interface adapts based on user permissions
- **Responsive Design**: Modern card-based layout with hover effects
- **Professional Typography**: Clear, readable fonts for business use

## 🔧 Testing

Run the validation script to verify system integrity:
```bash
python final_validation.py
```

## 📊 Data Management

### Staff Data Format
Staff information is stored in `Staff.txt` with the format:
```
username:id:password:role:salary
```

### Attendance Tracking
Check-in/check-out data is logged with timestamps in `Attendance.txt`

### Leave Requests
Leave applications are stored in `Leaves.txt` with approval status tracking

### Report System
Work reports are maintained in `Reports.txt` with manager comments and approval status

## 🔐 Security Features

- Password-protected authentication
- Role-based access control
- Session management
- Data validation and error handling

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure Python 3.7+ is installed with tkinter support
2. **Missing Files**: Run the application once to auto-create required data files
3. **Login Problems**: Use the default credentials listed above
4. **Permission Errors**: Check file write permissions in the application directory

### Support

If you encounter issues:
1. Run `python final_validation.py` to check system status
2. Verify all `.txt` files are present and readable
3. Check Python version compatibility
4. Ensure tkinter is properly installed

## 📝 Usage Guide

### For Managers
1. Log in with manager credentials
2. Access all three tabs: Essential, Management, Executive
3. Use "Manage Staff" to add new employees
4. Review reports in the "Review Reports" section
5. Generate attendance reports for oversight

### For HR Personnel
1. Log in with HR credentials
2. Access Essential and Management tabs
3. Handle staff management tasks
4. Process leave requests
5. Generate attendance summaries

### For General Staff
1. Log in with your assigned credentials
2. Use "Check In/Out" for daily attendance
3. Submit leave requests when needed
4. View your salary information
5. Submit daily work reports

## 🔄 Updates & Maintenance

The system automatically:
- Creates sample data on first run
- Maintains data file integrity
- Handles missing files gracefully
- Provides error logging and recovery

## 📋 Version Information

- **Version**: 1.0.0
- **Last Updated**: May 2025
- **Python Compatibility**: 3.7+
- **GUI Framework**: tkinter

---

🏨 **Hotel Staff Management System** - Professional staff management made simple.
