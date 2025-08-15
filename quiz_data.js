// Dummy quiz data organized by course
const quizzes = {
    computer_basics: [
      { id: 'quiz1', title: 'Computer Basics - Week 1' },
      { id: 'quiz2', title: 'Computer Basics - Week 2' },
      // Add more quizzes here
    ],
    advanced_programming: [
      { id: 'quiz3', title: 'Advanced Programming - Week 1' },
      // Add more quizzes here
    ],
    // Additional courses and quizzes as needed
  };
  
  // Function to get quizzes by course
  function getQuizzesForCourse(course) {
    return quizzes[course] || [];
  }
  