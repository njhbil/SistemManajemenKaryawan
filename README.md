# 🏨 Hotel Employee Management System

A comprehensive **Employee Management System** designed specifically for luxury hotels, built with Python and Tkinter. This system provides complete staff management functionality with a modern, elegant interface that reflects the luxury hospitality industry standards.

## ✨ Features

### 🔐 **Authentication & Security**
- Role-based access control (Manager, Admin, HR, etc.)
- Secure login system with encrypted user data
- Multi-level permission management

### 👥 **Staff Management**
- **Add New Staff**: Register new employees with complete information
- **View Staff Directory**: Comprehensive staff listing with details
- **Promotion System**: Update employee roles and salaries
- **Role Management**: Support for 6 different staff roles

### ⏰ **Attendance Tracking**
- Real-time check-in/check-out system
- Attendance history and reports
- Date-filtered attendance summaries
- Automatic timestamp recording

### 🏖️ **Leave Management**
- **Request Leave**: Submit leave applications with details
- **Approve/Reject**: Manager approval workflow
- **Leave Types**: Annual, Sick, Emergency, Personal leave
- **Leave History**: Track all leave requests and status

### 💰 **Payroll System**
- **Salary Management**: Update and track employee salaries
- **Bonus Calculation**: Role-based bonus system
- **Payroll Reports**: Comprehensive salary breakdowns
- **Salary History**: Track all salary changes with logging

### 📋 **Report Management**
- **Submit Reports**: Daily, weekly, and incident reports
- **Report Review**: Manager review and approval system
- **Report Types**: Multiple report categories
- **Status Tracking**: Pending, Approved, Rejected status

### 📊 **Dashboard & Analytics**
- **Live Statistics**: Real-time system overview
- **Staff Analytics**: Employee performance insights
- **System Status**: Database health monitoring
- **Live Clock**: Real-time date and time display

## 🎯 User Roles

| Role | Permissions |
|------|-------------|
| **Manager** | Full system access, approve leaves, review reports, manage payroll |
| **Admin** | Staff management, system administration, attendance reports |
| **Human Resource** | Employee data, leave management, payroll processing |
| **Marketing** | Report submission, attendance tracking, enhanced commission |
| **Cleaning Service** | Attendance, reports, room service management |
| **Internship** | Basic access, learning reports, guest service |

## 🖥️ User Interface

### **Login Screen**
- Elegant welcome panel with live system statistics
- Secure authentication form
- Real-time clock and system status
- Luxury hotel-themed design

### **Main Dashboard**
- Tabbed interface for organized functionality
- **Essential Operations**: Daily tasks and basic functions
- **Management**: Administrative and supervisory tools
- **Executive**: High-level management functions

### **Dialog Windows**
- Professional, responsive dialog boxes
- Form validation and error handling
- Consistent luxury theme throughout
- User-friendly navigation

## 🚀 Getting Started

### **Prerequisites**
- Python 3.7 or higher
- Tkinter (usually included with Python)
- Windows/Linux/MacOS

### **Installation**

1. **Clone the repository**
```bash
git clone https://github.com/njhbil/SistemManajemenKaryawan.git
cd SistemManajemenKaryawan
```

2. **Run the application**
```bash
python SistemManajemenKaryawan.py
```

### **Default Login Credentials**

| Role | Username | Staff ID | Password |
|------|----------|----------|----------|
| Manager | manager | 1001 | manager123 |
| Admin | admin | 1002 | admin123 |
| HR | hr | 1003 | hr123 |
| Cleaning | cleaning | 1004 | clean123 |
| Marketing | marketing | 1005 | market123 |
| Intern | intern | 1006 | intern123 |

## 📁 File Structure

```
Hotel-Employee-Management/
├── SistemManajemenKaryawan.py    # Main application file
├── Staff.txt                     # Employee database
├── Attendance.txt                # Attendance records
├── Leaves.txt                    # Leave requests
├── Reports.txt                   # Work reports
├── SalaryLog.txt                 # Salary change history
├── PromotionLog.txt              # Promotion history
└── README.md                     # This file
```

## 🔧 Technical Details

### **Architecture**
- **Object-Oriented Design**: Clean class hierarchy with inheritance
- **MVC Pattern**: Separation of data, logic, and presentation
- **File-based Database**: Simple text file storage system
- **Modular Components**: Reusable UI components and utilities

### **Key Classes**
- `Staff` (Abstract): Base class for all employee types
- `Manager`, `Admin`, `HumanResource`: Specific role implementations
- `HotelTheme`: Centralized UI theme management
- `SistemManajemenKaryawan`: Main application controller
- `LoginPage`, `MainMenuPage`: UI components

### **Data Storage**
- **Text Files**: Human-readable data storage
- **Colon-separated Values**: Simple parsing format
- **Automatic Backup**: Change logging for audit trails
- **Data Validation**: Input sanitization and error handling

## 🎨 Design Features

### **Color Scheme**
- **Primary Blue**: `#2196F3` - Modern, cheerful branding
- **Pure White**: `#FFFFFF` - Clean, professional background
- **Material Green**: `#4CAF50` - Success indicators
- **Material Red**: `#F44336` - Warning/error states

### **Typography**
- **Segoe UI**: Modern, readable font family
- **Hierarchical Sizing**: Clear information hierarchy
- **Consistent Styling**: Uniform appearance across components

### **User Experience**
- **Responsive Layout**: Adapts to different window sizes
- **Hover Effects**: Interactive feedback
- **Loading States**: Progress indicators
- **Error Handling**: User-friendly error messages

## 📈 System Statistics

The welcome screen displays real-time statistics:
- 👥 **Total Staff Count**
- ✅ **Today's Check-ins**
- 📋 **Pending Reports**
- 🏖️ **Pending Leave Requests**
- 🔧 **System Status**

## 🛡️ Security Features

- **Password Protection**: Secure login authentication
- **Role-based Access**: Permission-based feature access
- **Audit Logging**: Track all system changes
- **Data Validation**: Prevent invalid data entry
- **Session Management**: Secure user sessions

## 🔄 Future Enhancements

- 📱 **Mobile Application**: Cross-platform mobile app
- 🌐 **Web Interface**: Browser-based access
- 🗄️ **Database Integration**: MySQL/PostgreSQL support
- 📧 **Email Notifications**: Automated email alerts
- 📊 **Advanced Analytics**: Detailed reporting dashboard
- 🔔 **Push Notifications**: Real-time system alerts

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## ✅ TESTING COMPLETE - ALL FEATURES VERIFIED

### 🎯 Testing Results Summary:
- **Application Launch**: ✅ SUCCESSFUL - Starts without errors
- **UI Loading**: ✅ SUCCESSFUL - All beautification elements load properly
- **Missing Methods**: ✅ FIXED - All previously missing methods now implemented
- **Button Functionality**: ✅ WORKING - All dashboard buttons are functional
- **Authentication**: ✅ WORKING - Login system validates properly
- **Data Persistence**: ✅ WORKING - All data files integrate correctly

### 🔧 Issues Fixed During Testing:
1. **Missing `do_login` Method** - ✅ RESOLVED
   - Added complete authentication system
   - Validates credentials against Staff.txt
   - Creates appropriate user objects based on role
   - Handles login errors gracefully

2. **Missing `_create_luxury_card` Method** - ✅ RESOLVED
   - Added luxury-themed card creation system
   - Implements hover effects and visual feedback
   - Supports grid layout for dashboard organization
   - Integrates with existing theme system

3. **Missing `menu_laporan` Method** - ✅ RESOLVED
   - Added comprehensive report submission functionality
   - Role-based report templates and options
   - Auto-generated report templates based on user role
   - Proper integration with existing report system

### 🏨 Application Features Confirmed Working:
1. **Essential Operations Tab**:
   - ✅ Check In/Out functionality
   - ✅ Request Leave system
   - ✅ Submit Report with role-based templates

2. **Management Operations Tab** (Admin/HR/Manager):
   - ✅ Attendance Summary reports
   - ✅ Staff Management system
   - ✅ Leave Management approval system
   - ✅ Salary Management functionality

3. **Executive Operations Tab** (Manager only):
   - ✅ Report Review system
   - ✅ Team Analytics dashboard
   - ✅ Notification system

### 👥 Role-Based Access Control Verified:
- **Manager**: Full access to all management and executive features
- **Admin**: System administration and staff management features
- **HumanResource**: HR-specific features including leave and payroll management
- **Marketing**: Marketing-focused reporting and analytics
- **CleaningService**: Service-specific reporting and task management
- **Internship**: Learning-focused reporting and guest service features
