import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Register.css'; // Import local styles

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        name: '',
        age: '',
        city: ''
    });
    const [error, setError] = useState('');

    const navigate = useNavigate();
    const { username, password, name, age, city } = formData;

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async e => {
        e.preventDefault();
        const newUser = { username, password, name, age, city };
        try {
            const res = await axios.post(`${process.env.REACT_APP_HTTP_HOST}/users/register/`, newUser);
            console.log(res.data);
            localStorage.setItem("access", res.data.access);
            localStorage.setItem("refresh", res.data.refresh);
            navigate('/chat'); // Redirect to Login component after successful registration
        } catch (err) {
            console.error(err.response.data);
            setError(err.response.data.error); // Set error message as usual

        }
    };

    const goToLogin = () => {
        navigate('/login'); // Redirect to Login component
    };

    return (
        <div className="register-container"> {/* Use specific class name */}
            <h1>Register</h1>
            {error && <p className="error">{error}</p>} {/* Display error message */}
            <form onSubmit={onSubmit}>
                <input
                    type="text"
                    name="name"
                    placeholder="First Name"
                    value={name}
                    onChange={onChange}
                    required
                />
                <input
                    type="number"
                    name="age"
                    placeholder="Age"
                    value={age}
                    onChange={onChange}
                    required
                />
                <input
                    type="text"
                    name="city"
                    placeholder="City"
                    value={city}
                    onChange={onChange}
                    required
                />
                <input
                    type="username"
                    name="username"
                    placeholder="Username"
                    value={username}
                    onChange={onChange}
                    required
                />
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={password}
                    onChange={onChange}
                    required
                />
                <button type="submit" className="register-button">Register</button> {/* Use specific class name */}
            </form>
            <p>
                Already have an account?{' '}
                <span className="register-link" onClick={goToLogin}> {/* Use specific class name */}
                    Login
                </span>
            </p>
        </div>
    );
};

export default Register;
