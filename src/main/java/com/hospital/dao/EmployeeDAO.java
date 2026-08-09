package com.hospital.dao;

import com.hospital.model.Employee;
import com.hospital.util.DatabaseUtil;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

/**
 * Data Access Object for Employee entity
 */
public class EmployeeDAO {

    /**
     * Get all employees from the database
     * @return List of employees
     */
    public List<Employee> getAllEmployees() {
        List<Employee> employees = new ArrayList<>();
        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet rs = null;

        try {
            conn = DatabaseUtil.getConnection();
            String sql = "SELECT * FROM employees";
            stmt = conn.prepareStatement(sql);
            rs = stmt.executeQuery();

            while (rs.next()) {
                Employee emp = new Employee(
                    rs.getString("employee_id"),
                    rs.getString("name"),
                    rs.getInt("age"),
                    rs.getString("gender"),
                    rs.getDouble("salary"),
                    rs.getString("phone_number"),
                    rs.getString("email"),
                    rs.getString("role")
                );
                employees.add(emp);
            }
        } catch (SQLException e) {
            System.err.println("Error getting employees: " + e.getMessage());
        } finally {
            try {
                if (rs != null) rs.close();
                if (stmt != null) stmt.close();
            } catch (SQLException e) {
                System.err.println("Error closing resources: " + e.getMessage());
            }
            DatabaseUtil.closeConnection(conn);
        }

        return employees;
    }

    /**
     * Add a new employee to the database
     * @param emp Employee to add
     * @return true if successful, false otherwise
     */
    public boolean addEmployee(Employee emp) {
        Connection conn = null;
        PreparedStatement stmt = null;

        try {
            conn = DatabaseUtil.getConnection();
            String sql = "INSERT INTO employees (employee_id, name, age, gender, salary, phone_number, email, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
            stmt = conn.prepareStatement(sql);
            stmt.setString(1, emp.getEmployeeId());
            stmt.setString(2, emp.getName());
            stmt.setInt(3, emp.getAge());
            stmt.setString(4, emp.getGender());
            stmt.setDouble(5, emp.getSalary());
            stmt.setString(6, emp.getPhoneNumber());
            stmt.setString(7, emp.getEmail());
            stmt.setString(8, emp.getRole());

            int rowsAffected = stmt.executeUpdate();
            return rowsAffected > 0;
        } catch (SQLException e) {
            System.err.println("Error adding employee: " + e.getMessage());
            return false;
        } finally {
            try {
                if (stmt != null) stmt.close();
            } catch (SQLException e) {
                System.err.println("Error closing statement: " + e.getMessage());
            }
            DatabaseUtil.closeConnection(conn);
        }
    }
}
