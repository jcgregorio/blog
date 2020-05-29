/*
 *  Copyright (C) 2006 Oskar Linde
 *
 *  This software is provided 'as-is', without any express or implied
 *  warranty. In no event will the authors be held liable for any damages
 *  arising from the use of this software.
 *
 *  Permission is granted to anyone to use this software for any purpose,
 *  including commercial applications, and to alter it and redistribute it
 *  freely, in both source and binary form, subject to the following
 *  restrictions:
 *
 *  o  The origin of this software must not be misrepresented; you must not
 *     claim that you wrote the original software. If you use this software
 *     in a product, an acknowledgment in the product documentation would be
 *     appreciated but is not required.
 *  o  Altered source versions must be plainly marked as such, and must not
 *     be misrepresented as being the original software.
 *  o  This notice may not be removed or altered from any source
 *     distribution.
 */


/++
	<!--std.-->array is a collection of array template functions designed
	primarily to be applicable to D's built in array types. All array
	functions are designed to be usable as implicit array member functions.
	I.e the following are equivalent:
	---
	fun(arr,args);
	arr.fun(args);
	---
+/
module /*std.*/array;

/// Thrown by indexOf when no element is found
class ElementNotFoundException : Exception
{
    this() {
		super("ElementNotFound");
    }
}


version(MaxMinException) {
	/// Thrown by min/max when passed an empty array
	class EmptyArrayException : Exception
	{
		this() {
			super("EmptyArray");
		}
	}
}


// Private helper templates
private {
	// Return the element type X of an array X[]
	template ElementType(X) {
		alias typeof(X.ptr[0]) ElementType;
		//static if(is(ZeroLengthStaticArray!(X) E))
		//	alias E ElementType;
		//else
		//	alias typeof(declare!(X)[0]) ElementType;
	}
	
	
	// A declaration of X
	template Declare(X) { X Declare; }
	
	
	// To check for zero length static arrays
	template ZeroLengthStaticArray(X:X[0]) {
		alias X ZeroLengthStaticArray;
	}
	
	
	//Converts static arrays to dynamic arrays, leaving other types as they are
	template MakeDynamic(T) {
		static if( is(ZeroLengthStaticArray!(T) E)) // Workaround for segfault in DMD 0.149
			alias E[] MakeDynamic;
		else static if( is(typeof(Declare!(T).ptr[0]) E))
			static if (is(T:E[]))
				alias E[] MakeDynamic;
			else
				alias T MakeDynamic;
		else
			alias T MakeDynamic;
	}
}


///
template fold(Array,RetTy,FunTy) {
	/++
	Fold encapulates a simple pattern of recursion for processing arrays.
	This function recursively applies the function/delegate combiner on
	consecutive	elements of the array arr until only one element remains. It
	then returns that element. init is the first element fed to the combiner.
	The result is equivalent to:
	---
	combiner(init,fold(arr[1..$],arr[0],combiner));
	---
	Requirements_on_types:
	FunTy is a function/delegate:
	---
	RetTy fun(RetTy a, Elem b);
	---
	Array is anything that foreach can iterate over.

	Elem is anything implicitly convertible from the element type of Array.
	+/
	MakeDynamic!(RetTy) fold(Array arr, RetTy init, FunTy combiner) {
		MakeDynamic!(RetTy) ret = init;
		foreach(v;arr)
			ret = combiner(ret,v);
		return ret;
	}
}


// fold
unittest {
	const int[] a = [];
	const int[] b = [-5,1,5];
	int add(int a, int b) { return a+b; }
	assert(fold(a,0,&add) == 0);
	assert(fold(b,0,&add) == 1);
	
	int w = 1;
	assert(fold(b,0, delegate int(int a, int b) { return a + (w++) * b; }) == 1*-5+2*1+3*5);
	assert(w == 4);
	
	assert(fold(b,1, delegate int(int a, int b) { return a * b; }) == -25);

	assert("abcd".fold("", delegate char[](char[] a,char b) { return a ~ "+" ~ b; }) == "+a+b+c+d");
}

///
template findMax(Array,Pred) {
	/++
	Params:
	arr = non-empty array
	pred = an optional ordering predicate.
	Returns:
	The index of the maximum element of the array arr.
	size_t.max (-1) if the array is empty
	+/
	size_t findMax(Array arr,Pred pred) {
		alias ElementType!(Array) E;
		
		static if (is(ZeroLengthStaticArray!(Array)))
			return -1;
		else if (arr.length > 0) {
			size_t maxindex = 0;
			E maxel = arr[0];
			
			for(int i = 1; i < arr.length; i++)
				if (pred(arr[i],maxel))
					maxindex = i;

			return maxindex;
		}
		
		return -1;
	}
}

/// ditto
template findMax(Array) {
	size_t findMax(Array arr) {
		alias ElementType!(Array) E;

		return .findMax(arr,function bool(E a, E b) { return a > b; });
	}
}

///
template findMin(Array,Pred) {
	/++
	Params:
	arr = non-empty array
	pred = an optional ordering predicate.
	Returns:
	The index of the minimum element of the array arr.
	size_t.max (-1) if the array is empty
	+/
	size_t findMin(Array arr,Pred pred) {
		alias ElementType!(Array) E;

		// reverse the predicate and return findMax
		return .findMax(arr,delegate bool(E a, E b) { return pred(b,a); });
	}
}

/// ditto
template findMin(Array) {
	size_t findMin(Array arr) {
		alias ElementType!(Array) E;

		return .findMin(arr,function bool(E a, E b) { return a > b; });
	}
}

///
template max(Array,Pred) {
	/++
	Params:
	arr = non-empty array
	pred = an optional ordering predicate.
	Returns:
	The maximum element of the array arr.
	+/
	ElementType!(Array) max(Array arr,Pred pred)
	in {
		version(MaxMinException) {} else { assert(arr.length > 0); }
	} body {
		alias ElementType!(Array) E;
		version(MaxMinException) {
			if (arr.length == 0)
				throw new EmptyArrayException;
		}
		return arr[arr.findMax(pred)];
	}
}


/// ditto
template max(Array) {
	ElementType!(Array) max(Array arr) {
		alias ElementType!(Array) E;
		return .max(arr, function bool(E a, E b) { return a > b; });
	}
}


///
template min(Array,Pred) {
	/++
	Params:
	arr = non-empty array
	pred = an optional ordering predicate.
	Returns:
	The minimum element of the array arr.
	+/
	ElementType!(Array) min(Array arr,Pred pred)
	in {
		version(MaxMinException) {} else { assert(arr.length > 0); }
	} body {
		alias ElementType!(Array) E;
		version(MaxMinException) {
			if (arr.length == 0)
				throw new EmptyArrayException;
		}
		 // reverse pred
		return arr[arr.findMin(pred)];
	}
}


/// ditto
template min(Array) {
	ElementType!(Array) min(Array arr) {
		alias ElementType!(Array) E;
		return .min(arr, function bool(E a, E b) { return a > b; });
	}
}


// max, min, findMax, findMin
unittest {
	const int[] a = [-5,1,100];
	assert(a.max() == 100);
	assert(a.min() == -5);
	assert(a.findMax() == 2);
	assert(a.findMin() == 0);
	const int[] b = [];
	version(MaxMinException) {
		try {
			b.max();
			assert(0);
		} catch (EmptyArrayException e) {}
		try {
			b.max();
			assert(0);
		} catch (EmptyArrayException e) {}
		try {
			"".max();
			assert(0);
		} catch (EmptyArrayException e) {}
		try {
			"".min();
			assert(0);
		} catch (EmptyArrayException e) {}
	}
	assert("".findMin() == -1);
	assert("".findMax() == -1);
	char[] t = "";
	assert(t.findMin() == -1);
	assert(t.findMax() == -1);
	assert("abcd".max() == 'd');
	assert("abcd".findMax() == 3);
	assert("abcd".max(function bool(char a, char b) { return a < b; }) == 'a');
	assert("abcd".findMax(function bool(char a, char b) { return a < b; }) == 0);
	assert("abcd".min() == 'a');
	assert("abcd".findMin() == 0);
	assert("abcd".min(function bool(char a, char b) { return a < b; }) == 'd');
	assert("abcd".findMin(function bool(char a, char b) { return a < b; }) == 3);
}


///
template indexOf(Array,Elem) {
    /++
	Params:
	arr = array
	e = element to be found or a function/delegate predicate
	Returns:
	The index of the first occurence of e in arr or the first element in arr where the predicate is true.
	Throws:
	ElementNotFoundException
	+/
	size_t indexOf(Array arr, Elem e) {
		size_t i = find(arr,e);
		if (i == -1)
			throw new ElementNotFoundException;
		return i;
	}
}


private template IsCharacterType(E) {
	const IsCharacterType = (is(E == char) || is(E == dchar) || is(E == wchar));
}

private import std.utf;

private template findImpl(bool reverse, Array, Elem) {
	size_t findImpl(Array arr, Elem e) {
		static if (is(Elem == function) || is(Elem == delegate)) {
			// Search delegate, function
			static if (reverse) {
				for(int ix = arr.length-1; ix >= 0; ix--)
					if (e(arr[ix]))
						return ix;
			} else {
				foreach(size_t ix, a; arr)
					if (e(a))
						return ix;
			}
			return -1;
		} else static if (is(Elem : ElementType!(Array))) {
			alias ElementType!(Array) E;
			// Element search
			// Support foreach(dchar;char[]) etc...
			static if (IsCharacterType!(E) && IsCharacterType!(Elem) &&
			           Elem.sizeof > E.sizeof) {
				// Transform element search into subarray search
				static if (is(E == wchar)) {
					wchar[2] storage;
					wchar[] str = std.utf.toUTF16(storage,e);
					return .findImpl!(reverse,Array,wchar[])(arr,str);
				} else static if (is(E == char)) {
					char[4] storage;
					char[] str;
					str = toUTF8(storage,e);
					return .findImpl!(reverse,Array,char[])(arr,str);
				} else static assert(0);	
			} else {
				static if (reverse) {
					for (int ix = arr.length-1; ix >= 0; ix--)
						if (arr[ix] == e)
							return ix;
				} else {
					foreach (uint ix, a; arr)
						if (a == e)
							return ix;
				}
				return -1;
			}
		} else {
			// subarray search
			static if (is(ZeroLengthStaticArray!(Elem))) {
				static if (reverse)
					return arr.length;
				else
					return 0;
			} else {
				if (e.length == 0) {
					static if (reverse)
						return arr.length;
					else
						return 0;
				}
				if (e.length == 1)
					return .find(arr,e[0]);
				if (e.length > arr.length) // avoid unsigned underflow below
					return -1;
				static if (reverse) {
					outer: for (int i = arr.length-e.length; i >= 0; i--) {
						for (int j = 0; j < e.length; j++)
							if (arr[i+j] != e[j])
								continue outer;
						return i;
					}
				} else {
					outer: for (int i = 0; i <= arr.length - e.length; i++) {
						for (int j = 0; j < e.length; j++)
							if (arr[i+j] != e[j])
								continue outer;
						return i;
					}
				}
				return -1;
			}
		}
	}
}


///
template find(Array,Elem) {
	/++
	Params:
	arr = array
	e = element, function/delegate predicate or a subarray
	Returns:
	The index of the first occurence of e in arr or the first element in arr where the predicate is true.

	size_t.max (-1) if not found
	+/
	size_t find(Array arr, Elem e) {
		return findImpl!(false,Array,Elem)(arr,e);
	}
}

///
template rfind(Array,Elem) {
	/++
	Params:
	arr = array
	e = element, function/delegate predicate or a subarray
	Returns:
	The index of the last occurence of e in arr or the last element in arr where the predicate is true.

	size_t.max (-1) if not found
	+/
	size_t rfind(Array arr, Elem e) {
		return findImpl!(true,Array,Elem)(arr,e);
	}
}

// indexOf, find and rfind
unittest {
	const int[] arr = [0,1,2,3,4,5,6];
	foreach(e;arr) {
		assert(arr.indexOf(e) == e);
		assert(arr.find(e) == e);
	}
	try {
		arr.indexOf(7);
		assert(0);
	} catch (ElementNotFoundException e) { }
	assert("abc".find("") == 0);
	assert("abc".rfind("") == 3);
	assert("åäö".find('å') == 0);
	assert("åäö".find('ä') == 2);
	assert("åäö".find('ö') == 4);
	assert("åäö".rfind('å') == 0);
	assert("åäö".rfind('ä') == 2);
	assert("åäö".rfind('ö') == 4);
	char[] t = "";
	assert(t.find("a") == -1);
	assert(t.rfind("a") == -1);
	assert("☃☠☢☮☯☺☼♨".find('☺') == 15);
	assert("☃☠☢☮☯☺☼♨".find("☺") == 15);
	assert("☃☠☢☮☯☺☼♨".find("☺☼") == 15);
	assert("☃☠☢☮☯☺☼♨abc☺".find("abc") == 24);
	assert("☃☠☢☮☯☺☼♨abc☺"c.find('a') == 24);
	assert("☃☠☢☮☯☺☼♨abc☺"w.find('a') == 8);
	assert("☃☠☢☮☯☺☼♨abc☺"d.find('a') == 8);
	assert("𝌁𝌂𝌃𝌄"c.find('𝌄') == 12);
	assert("𝌁𝌂𝌃𝌄"w.find('𝌄') == 6);
	assert("𝌁𝌂𝌃𝌄"d.find('𝌄') == 3);
	assert("𝌁𝌂𝌃𝌄"c.find("𝌄"c) == 12);
	assert("𝌁𝌂𝌃𝌄"w.find("𝌄"w) == 6);
	assert("𝌁𝌂𝌃𝌄"d.find("𝌄"d) == 3);
	assert(arr.find(arr[3..5]) == 3);
	assert(arr.find(arr[0..1]) == 0);
	assert(arr.find(arr[$-1..$]) == arr.length-1);
	assert(arr.find(arr[$-2..$]) == arr.length-2);
	assert(arr.find(arr[$-2..$-1]) == arr.length-2);
	assert(arr.find(7) == -1);
	assert(arr.indexOf(delegate bool(int x) { return x >= 2; }) == 2);
	assert(arr.find(delegate bool(int x) { return x >= 2; }) == 2);
	assert(arr.rfind(delegate bool(int x) { return x >= 2; }) == 6);
	assert(arr.rfind(delegate bool(int x) { return x < 2; }) == 1);
	foreach(e;arr) {
		assert(arr.indexOf(delegate bool(int x) { return x == e; }) == e);
		assert(arr.find(delegate bool(int x) { return x == e; }) == e);
	}
	try {
		arr.indexOf(delegate bool(int x) { return x > 6; });
		assert(0);
	} catch (ElementNotFoundException e) {}
	assert(arr.find(delegate bool(int x) { return x > 6; }) == -1);
	assert("".find('x') == -1);
	assert("abababab".find("ab") == 0);
	assert("abababab".rfind("ab") == 6);
	assert("aba".find("ababa") == -1);
	assert("aba".rfind("ababa") == -1);
	assert("".find("ab") == -1);
	assert("".rfind("ab") == -1);
	assert("aaa".find("aaa") == 0);
	assert("aaa".rfind("aaa") == 0);
	assert("abc def".split(' ').find("def") == 1);
	try {
		"".indexOf('x');
		assert(0);
	} catch (ElementNotFoundException e) {}
}


///
template split(Array,Delim) {
	/++
	Splits the array arr into an array of subarrays of arr.
	Params:
	delim = element, array of elements or predicate on which the array should be split.
	+/
	ElementType!(Array)[][] split(Array arr, Delim delim) {
		//static if (is(Delim == function) || is(Delim == delegate)) {
		ElementType!(Array)[][] ret;
		uint i,j;

		i = 0;
		while (i < arr.length) {
			j = find(arr[i..$], delim);
			if (j == -1) {
				ret ~= arr[i..$];
				break;
			}
			ret ~= arr[i..i+j];
			static if( is(MakeDynamic!(Delim) == MakeDynamic!(Array)))
				i += j+delim.length;
			else
				i += j+1;
			if (i == arr.length) {
				ret ~= arr[$..$];
				break;
			}
		}
		return ret;
	}
}


///
template join(Array,Elem) {
	/++
	Concatenate all elements of an array, using an optional separator
	Params:
	delim = single element or array of elements
	+/
	ElementType!(Array) join(Array arr, Elem delim) {
		ElementType!(Array) ret = null;
		ElementType!(Array) del;
		foreach(a; arr) {
			ret ~= del;
			ret ~= a;
			static if(is(MakeDynamic!(Elem) == ElementType!(Array)))
				del = delim[];
			else
				del = (&delim)[0..1];
		}
		return ret;
	}
}


/// ditto
template join(Array) {
	/// 
	ElementType!(Array) join(Array arr) {
		ElementType!(Array) ret = null;
		ElementType!(Array) del;
		foreach(a; arr) {
			ret ~= a;
		}
		return ret;
	}
}


// split and join
unittest {
	assert("a b c d e f".split(' ').join('.') == "a.b.c.d.e.f");
	assert("a b c".split(delegate bool(char x) { return x >= 'a' && x <= 'z'; }).join('-') == "- - -");
	assert("a b c".split(delegate bool(char x) { return "abcdefg".find(x) != -1;}).join('-') == "- - -");
	assert("ababcdabacabab".split("ab").join() == "cdac");
	assert("".split(' ').length == 0);
	assert("".split(" ").length == 0);
	assert(" ".split(' ').length == 2);
	assert(" ".split(" ").length == 2);
	assert("".split(" ").join("") == "");
	const char[][] d = [['x']];
	assert("a.x.a.x.a.x.a.x".split('.').split(d).join("".split(' ')).join("") == "aaaa");
	assert(" a b c d e f ".split(" ").join(" ") == " a b c d e f ");
	assert(" a b c d e f ".split(" ").join(' ') == " a b c d e f ");
	assert(" a b c d e f ".split(' ').join(" ") == " a b c d e f ");
	assert(" a b c d e f ".split(' ').join(' ') == " a b c d e f ");
	assert("  a  b  c  d  e  f  ".split("  ").join(" ") == " a b c d e f ");
	assert("  a  b  c  d  e  f  ".split("  ").join(' ') == " a b c d e f ");
	assert("   .   .   .".split("  ").join() == " . . .");
	assert("a b c d".split(' ').join() == "abcd");
	assert("a b c d".split(' ').join("") == "abcd");
	assert("a b c".split(' ').join("--") == "a--b--c");
}


// The return type of a function type FunTy taking 1 argument of type ArgTy
private template RetType(FunTy,ArgTy) { alias typeof(Declare!(FunTy)(ArgTy.init)) RetType; }


///
template map(Array, FunTy) {
	/++
	Map an array over the given function/delegate, returning an array of
	the result
	 +/
	 RetType!(FunTy,ElementType!(Array))[] map(Array arr, FunTy fun) {
		RetType!(FunTy,typeof(arr.ptr[0]))[] ret;
		ret.length = arr.length;
		foreach(uint i, t; arr)
			ret[i] = fun(t);
		return ret;
	}
}


/// 
template doMap(Array, FunTy) {
	/// inplace version of map()
	void doMap(Array arr, FunTy fun) {
		foreach(inout t; arr)
			t = fun(t);
	}
}


unittest {
	const int[] d = [0,1,2,3,4,5];
	auto b = d.map(function float(int x) { return x/2.0; });
	static assert(is(typeof(b) == float[]));
	foreach(ix,f;b)
		assert(f == ix/2.0);
	auto c = d.map(delegate int(int x) { return x*2; });
	foreach(ix,i;c)
		assert(i == ix*2);
	char upperCase(char c) { return c >= 'a' && c <= 'z' ? c + 'A' - 'a' : c; }
	assert(map("",&upperCase) == "");
	assert(map("abcd1234",&upperCase) == "ABCD1234");
	char[] t = "a!c".dup;
	char *ptr = t.ptr;
	t.doMap(&upperCase);
	assert(t == "A!C");
	assert(t.ptr == ptr);
	static assert(!is(typeof(d.doMap(function float(int x) { return x/2.0; }))));
}


///
template filter(Array, Pred) {
	/++
	Maps the array arr over the given predicate pred. Returns an array of the elements
	for which the predicate is true
	+/
	MakeDynamic!(Array) filter(Array arr, Pred pred) {
		MakeDynamic!(Array) ret;
		foreach(a; arr)
			if (pred(a))
				ret ~= a;
		return ret;
	}
}


import std.stdio;

///
template count(Array,Pred) {
	/++
	Returns:
	A count of the number of elements of arr where the predicate pred is true
	+/
	size_t count(Array arr,Pred pred) {
		alias ElementType!(Array) E;
		int n = 0;
		static if( is(Pred == function) || is(Pred == delegate)) {
			foreach(e;arr)
				if (pred(e))
					n++;
		} else {
			int i;
			MakeDynamic!(Array) tmp = arr;
			while(1) {
				i = tmp.find(pred);
				if (i == -1)
					break;
				n++;
				static if (is(typeof(pred.length)))
					tmp = tmp[i+pred.length..$];
				else
					tmp = tmp[i+1..$];
			}
		}
		return n;
	}
}


unittest {
	bool isLowerCase(char c) { return c >= 'a' && c <= 'z'; }
	assert("".filter(&isLowerCase)=="");
	assert("aBc".filter(&isLowerCase)=="ac");
	assert("abc".filter(&isLowerCase)=="abc");
	assert("ABC".filter(&isLowerCase)=="");
	assert("".count(&isLowerCase)==0);
	assert("aBc".count(&isLowerCase)==2);
	assert("abc".count(&isLowerCase)==3);
	assert("ABC".count(&isLowerCase)==0);
	assert("abc".count('a') == 1);
	assert("abc".count('d') == 0);
	assert("aabaab".count('a') == 4);
	assert("abababab".count("ab") == 4);
	assert("ab".count("ab") == 1);
	assert("".count("ab") == 0);
	assert("aaa".count("aa") == 1);
	assert("aaaa".count("aa") == 2);
	assert("aaaaa".count("aa") == 2);
	assert("aaåäöa".count('å') == 1);
	assert("åäöåäö".count('å') == 2);
	
}


///
template sort(Array,Pred) {
	/++
	Return a sorted version of array arr.
	Params:
	wrongOrder = optional binary ordering predicate
	+/
	MakeDynamic!(Array) sort(Array arr, Pred wrongOrder) {
		MakeDynamic!(Array) ret = arr.dup;
		ret.doSort(wrongOrder);
		return ret;
	}
}


/// ditto
template sort(Array) {
	MakeDynamic!(Array) sort(Array arr) {
		MakeDynamic!(Array) ret = arr.dup;
		ret.doSort();
		return ret;
	}
}


///
template doSort(Array, Pred) {
	/++ 
	Sort the elements of the array inplace. Not stable.
	params:
	wrongOrder = optional ordering predicate
	+/
	void doSort(Array array, Pred wrongOrder) {
		alias ElementType!(Array) E;

		void swap(inout E a, inout E b) {
			E tmp = a;
			a = b;
			b = tmp;
		}
		
		int partition(MakeDynamic!(Array) arr) {
			size_t l = arr.length-1;
			size_t up = 1;
			size_t down = l;
			assert(l >= 1);

			// pick the median of first, last and middle
			// sort so that arr[1] <= pivot <= arr[$-1]
			
			swap(arr[0],arr[l/2]);
			
			if(wrongOrder(arr[1],arr[l]))
				swap(arr[1],arr[l]); // sort first, last
			if(wrongOrder(arr[1],arr[0]))
				swap(arr[1],arr[0]);
			else if(wrongOrder(arr[0],arr[l]))
				swap(arr[0], arr[l]);
				
			E pivot = arr[0];
			
			while(1) {
				do 
					up++;
				while(wrongOrder(pivot,arr[up]))
					
				do
					down--;
				while(wrongOrder(arr[down],pivot))
					
				if (up > down)
					break;
				swap(arr[up],arr[down]);
			}
			
			arr[0] = arr[down];
			arr[down] = pivot;

			debug foreach(i;arr[0..down])
				assert(!wrongOrder(i,pivot));
			debug foreach(i;arr[down+1..$])
				assert(!wrongOrder(pivot,i));
			
			return down;
		}

		const int stackSize = 40;
		Array[stackSize] stack;
		int sp = 0;
		MakeDynamic!(Array) arr;
		const int threshold = 7;
		
		arr = array;
		while(1) {
			while (arr.length > threshold) {
				int pivotIndex = partition(arr);
				if (pivotIndex > arr.length/2) {
					stack[sp++] = arr[pivotIndex+1..$];
					arr = arr[0..pivotIndex];
				} else {
					stack[sp++] = arr[0..pivotIndex];
					arr = arr[pivotIndex+1..$];
				}
				assert(sp <= stackSize);
			}
			
			// insertion sort
			for (int i = 1; i < arr.length; i++) 
				for (int j = i; j > 0 && wrongOrder(arr[j-1],arr[j]); j--) 
					swap(arr[j-1],arr[j]);	
			
			// recurse
			if (sp > 0) 
				arr = stack[--sp];
			else
				return;
		}
		
	}
}


/// ditto
template doSort(Array) {
	// Copy paste of above implementation
	// the code without ordering predicate is ~2.5 times faster
	void doSort(Array array) {
		alias ElementType!(Array) E;

		void swap(inout E a, inout E b) {
			E tmp = a;
			a = b;
			b = tmp;
		}
		
		int partition(MakeDynamic!(Array) arr) {
			size_t l = arr.length-1;
			size_t up = 1;
			size_t down = l;
			assert(l >= 1);

			// pick the median of first, last and middle
			
			swap(arr[0],arr[l/2]);
			
			if(arr[1] > arr[l])
				swap(arr[1],arr[l]); // sort first, last
			if(arr[1] > arr[0])
				swap(arr[1],arr[0]);
			else if(arr[0] > arr[l])
				swap(arr[0], arr[l]);
				
			E pivot = arr[0];
			
			while(1) {
				do 
					up++;
				while(/*up < l &&*/ arr[up] < pivot)
					
				do
					down--;
				while(arr[down] > pivot/* && down > 1*/)
					
				if (up > down)
					break;
				swap(arr[up],arr[down]);
			}
			
			arr[0] = arr[down];
			arr[down] = pivot;

			debug foreach(i;arr[0..down])
				assert(i <= pivot);
			debug foreach(i;arr[down+1..$])
				assert(i >= pivot);
			
			return down;
		}

		const int stackSize = 40;
		Array[stackSize] stack;
		int sp = 0;
		MakeDynamic!(Array) arr;
		const int threshold = 7;
		
		arr = array;
		while(1) {
			while (arr.length > threshold) {
				int pivotIndex = partition(arr);
				if (pivotIndex > arr.length/2) {
					stack[sp++] = arr[pivotIndex+1..$];
					arr = arr[0..pivotIndex];
				} else {
					stack[sp++] = arr[0..pivotIndex];
					arr = arr[pivotIndex+1..$];
				}
				assert(sp < stackSize);
			}
			
			// insertion sort
			for (int i = 1; i < arr.length; i++) 
				for (int j = i; j > 0 && (arr[j-1] > arr[j]); j--) 
					swap(arr[j-1],arr[j]);	
			
			// recurse
			if (sp > 0) 
				arr = stack[--sp];
			else
				return;
		}
		
	}
}


///
template doStableSort(Array, Pred) {
	/// stable in-place array sort
	void doStableSort(Array arr, Pred wrongOrder) {
		alias MakeDynamic!(Array) DynArr;
		DynArr tmp;
		
		void merge(DynArr arr, size_t mid) {
			size_t i,j,k;
			
			// save away first half of array
			i = 0; j = 0;
			while (j < mid)
				tmp[i++] = arr[j++];
			
			// merge arrays
			i = 0; 	k = 0;
			while (k < j && j < arr.length)
				if (!wrongOrder(tmp[i],arr[j]))
					arr[k++] = tmp[i++];
				else
					arr[k++] = arr[j++];
			
			// copy remaining tmp elements
			while (k < j)
				arr[k++] = tmp[i++];
		}
		
		void mergesort(DynArr arr) {
			if (arr.length <= 1)
				return;
			size_t mid = arr.length/2;
			mergesort(arr[0..mid]);
			mergesort(arr[mid..$]);
			merge(arr, mid);
		}
		
		tmp.length = (arr.length+1)/2;
		mergesort(arr[]);
	}
}


/// ditto
template doStableSort(Array) {
	void doStableSort(Array arr) {
		.doStableSort(arr,function bool(ElementType!(Array) a, ElementType!(Array) b) { return a > b; });
	}
}


///
template stableSort(Array, Pred) {
	/// Returns a sorted version of array arr. The sort is stable.
	MakeDynamic!(Array) stableSort(Array arr, Pred wrongOrder) {
		MakeDynamic!(Array) ret = arr.dup;
		ret.doStableSort(wrongOrder);
		return ret;
	}
}


/// ditto
template stableSort(Array) {
	MakeDynamic!(Array) stableSort(Array arr) {
		MakeDynamic!(Array) ret = arr.dup;
		ret.doStableSort(function bool(ElementType!(Array) a, ElementType!(Array) b) { return a > b; });
		return ret;
	}
}


debug private template SortUnitTest(alias sort, alias doSort) {
	void SortUnitTest() {
		const int[] arr = [1,2,4,2,1,4,6,8,3,1,4];
		int[] arrc = arr.dup;
		int[] arr2 = arr.sort();
		assert(arr2 != arr);
		assert(arrc == arr);
		// Same length
		assert(arr2.length == arr.length);
		// Ascending order
		for (int i = 1; i < arr2.length; i++)
			assert(arr2[i-1] <= arr2[i]);
		// Same count for each element
		foreach(x;arr) {
			assert(count(arr,delegate bool(int v) { return v == x; }) ==
			count(arr2,delegate bool(int v) { return v == x; }));
		}
		assert("ab".sort() == "ab");
		assert("ba".sort() == "ab");
		assert("abc".sort() == "abc");
		assert("acb".sort() == "abc");
		assert("bac".sort() == "abc");
		assert("bca".sort() == "abc");
		assert("cab".sort() == "abc");
		assert("cba".sort() == "abc");
		assert("daceb".sort() == "abcde");
		assert("becad".sort() == "abcde");
		assert("aaaaaab".sort() == "aaaaaab");
		assert("aaaaaba".sort() == "aaaaaab");
		assert("aaaabaa".sort() == "aaaaaab");
		assert("aaabaaa".sort() == "aaaaaab");
		assert("aabaaaa".sort() == "aaaaaab");
		assert("abaaaaa".sort() == "aaaaaab");
		assert("baaaaaa".sort() == "aaaaaab");
		assert("aaabaab".sort() == "aaaaabb");
		assert("aaababa".sort() == "aaaaabb");
		assert("aaabbaa".sort() == "aaaaabb");
		assert("aabbaaa".sort() == "aaaaabb");
		assert("aabbaaa".sort() == "aaaaabb");
		assert("ababaaa".sort() == "aaaaabb");
		assert("baabaaa".sort() == "aaaaabb");
		assert("daceb".sort(delegate bool(char a, char b) { return a < b; }) == "edcba");
		assert("earcvsqygktdxjnpbfzuomwihl".sort() == "abcdefghijklmnopqrstuvwxyz");
		assert("earcvsqygktdxjnpbfzuomwihl".sort(delegate bool(char a, char b) { return a > b; }) == "abcdefghijklmnopqrstuvwxyz");
		assert("bcccbbabcccaabbcccccccccacbccacaccccaccbcacacccccacaabaccacc".sort() ==
		       "aaaaaaaaaaaaaabbbbbbbbbccccccccccccccccccccccccccccccccccccc");
		char[] t = "becad".dup;
		t.doSort();
		assert(t == "abcde");
	}
}


// sort, doSort, stableSort, doStableSort
unittest {
	SortUnitTest!(sort,doSort)();
	SortUnitTest!(stableSort,doStableSort)();
	
	// Check stability
	struct T { int a; int b; }	
	const T[] arr = [{1,1},{8,1},{1,6},{3,2},{1,2},{7,3},{7,1},{7,5},{1,6}];
	const T[] stableSorted = [{1,1},{1,6},{1,2},{1,6},{3,2},{7,3},{7,1},{7,5},{8,1}];
	T[] arr2 = arr.dup;
	bool cmpTa(inout T a, inout T b) { return a.a > b.a; }
	arr2.doStableSort(&cmpTa);
	//writefln(arr2.map(function char[] (T a) { return "{" ~ cast(char)('0'+a.a) ~ "," ~ cast(char) ('0'+a.b) ~ "}"; }));
	assert(arr2 == stableSorted);
	T[] arr3 = arr.stableSort(&cmpTa);
	assert(arr3 == stableSorted);
}


///
template reverse(Array) {
	/// Return a reversed copy of a given array
	MakeDynamic!(Array) reverse(Array arr) {
		MakeDynamic!(Array) ret;
		ret.length = arr.length;
		size_t last = arr.length-1;
		foreach(size_t ix, e; arr)
			ret[last-ix] = e;
		return ret;
	}
}


///
template doReverse(Array) {
	/// In-place reverse the contents of the given array
	void doReverse(Array arr) {
		alias ElementType!(Array) E;
		void swap(inout E a, inout E b) {
			E tmp = a;
			a = b;
			b = tmp;
		}
	
		size_t half = arr.length/2;
		for (int i = 0; i < half; i++)
			swap(arr[i],arr[$-i-1]);
	}
}


// reverse,doReverse
unittest {
	assert("abcd".reverse() == "dcba");
	assert("abc".reverse() == "cba");
	assert("ab".reverse() == "ba");
	assert("a".reverse() == "a");
	auto a = "abcd";
	assert(a.reverse() == "dcba");
	assert(a == "abcd");
	auto b = "abcd".dup;
	b.doReverse();
	assert(b == "dcba");
	auto c = "abc".dup;
	c.doReverse();
	assert(c == "cba");
	auto d = "ab".dup;
	d.doReverse();
	assert(d == "ba");
	auto e = "a".dup;
	e.doReverse();
	assert(e == "a");
}

///
template repeat(Array, Integer) {
	/// Repeats the given array n times
	MakeDynamic!(Array) repeat(Array arr, Integer n) {
		static if (is(ZeroLengthStaticArray!(Array))) {
			return null;
		} else {
			if (n == 0)
				return null;
			if (n == 1)
				return arr;
				
			MakeDynamic!(Array) ret = new ElementType!(Array)[arr.length * n];
			if (arr.length == 1) {
				ret[] = arr[0];
			} else {
				size_t len = arr.length;
				for (int i = 0; i < len*n; i += len)
					ret[i..i+len] = arr;
			}
			return ret;
		}
	}
}

// repeat
unittest {
	assert("12".repeat(3) == "121212");
	assert("".repeat(5) == "");
	assert("12".repeat(0) == "");
	assert("12".repeat(1) == "12");
}

